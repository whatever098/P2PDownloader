import logging
import random
import re
import socket
import struct
import urllib.parse
import aiohttp
import asyncudp
from aiohttp import ClientSession
from asyncudp import Socket
from typing import Optional
from src.torrent import bencoding
from src.torrent.torrent import Torrent

"""
    @filename tracker.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0

    该模块实现了和Tracker服务器的通信,目前支持http协议和udp协议
    实现了封装类Tracker,和Tracker服务器通信
    实现了封装类TrackerResponse,通过peers属性访问peers的(ip,port)
"""


def _decode_port(port):
    """
    按照网络大端存储模式解析port（无符号短整型H）
    """
    return struct.unpack(">H", port)[0]


class TrackerResponse:
    def __init__(self, response, use_udp):
        self.response = response
        self.use_udp = use_udp  # 是否为使用udp的tracker

    @property
    def failure(self):
        if b'failure reason' in self.response:
            return self.response[b'failure reason'].decode('utf-8')
        return None

    @property
    def interval(self) -> int:
        """
        可选参数,客户端在向跟踪器发送常规请求之间应等待的时间间隔（以秒为单位）
        """
        return self.response.get(b'interval', 0)

    @property
    def complete(self) -> int:
        """
        可选参数,有多少个完整的结点
        """
        return self.response.get(b'complete', 0)

    @property
    def incomplete(self) -> int:
        """
        可选参数,有多少个不完整的结点
        """
        return self.response.get(b'incomplete', 0)

    @property
    def peers(self) -> []:
        """
         :return: 返回一个列表,列表中的每一项是peer的信息 (ip,port,use_udp)
        """
        peers = self.response.get(b'peers', [])
        if type(peers) == list:
            logging.debug('Dictionary model peers are returned by tracker')
            return []
        else:
            logging.debug('Binary model peers are returned by tracker')

            peers = [peers[i:i + 6] for i in range(0, len(peers), 6)]
            return [(socket.inet_ntoa(p[:4]), _decode_port(p[4:]), self.use_udp) for p in peers]


def _calculate_peer_id():
    """
    返回标识自己主机的peer id
    :return: this client's peer id
    """
    return '-PC0223-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])


def int_to_IP(ip):
    """
    将十进制数字转换为IP地址字符串
    :param ip: 十进制数字
    :return: IP地址字符串
    """
    # 将十进制数转换为32位二进制字符串
    binary_string = format(ip, '032b')
    # 将32位二进制字符串分成四个8位组
    octets = [binary_string[i:i + 8] for i in range(0, 32, 8)]
    # 将每个8位二进制组转换为十进制数
    decimal_octets = [int(octet, 2) for octet in octets]
    # 将四个十进制数合并为IP地址
    ip_address = ".".join(map(str, decimal_octets))
    return ip_address


class Tracker:
    def __init__(self, torrent: Torrent, announce):
        """
        :param torrent: Torrent类的实例
        """
        self.torrent = torrent
        self.peer_id = _calculate_peer_id()  # urlen编码的 20 字节字符串
        self.http_client: Optional[ClientSession] = None
        self.sock: Optional[Socket] = None
        self.use_udp = announce.startswith("udp")
        self.announce = announce  # 请求url
        self.previous = 0
        self.can_connect = True  # 标识第一次连接是否成功

    async def connect(self, first: bool = False, downloaded: int = 0, uploaded: int = 0) -> TrackerResponse:
        """
        根据announce的类型来决定是使用http协议还是udp协议，随后进行连接
        :param first: 是否是第一次下载
        :param downloaded: 已经下载的字节数
        :param uploaded:  上传的字节数
        :return: TrackerResponse: 对通信结果的封装
        :raise: ConnectionError: Unable to connect to tracker
        """
        if self.use_udp:  # 使用udp://协议的tracker
            try:
                self.can_connect = True
                match = re.search(r'udp://([^:/]+:\d+)/', self.announce)
                if match:
                    tracker_address = match.group(1)
                    remote_ip, remote_port = tracker_address.split(":")  # 主机名与端口
                    remote_port = int(remote_port)
                else:
                    raise ConnectionError('Unable to connect to udp tracker')
                if self.sock is None:
                    self.sock = await asyncudp.create_socket(remote_addr=(remote_ip, remote_port))

                connect_request = struct.pack('>QII', 0x41727101980, 0, 99)  # transaction id...
                self.sock.sendto(connect_request)
                datagram, remote_addr = await self.sock.recvfrom()  # 收到tracker返回的数据报（类似ACK）
                action, transaction_id, connection_id = struct.unpack('>IIQ', datagram)
                if not action == 0 and not transaction_id == 99:  # id不对应
                    raise ConnectionError('Unable to connect to tracker')
                announce_request = struct.pack(
                    '>QII20s20sQQQIIIiH',
                    connection_id,  # Connection ID
                    1,  # Action (Announce请求)
                    99,  # Transaction ID
                    self.torrent.info_hash,  # Info hash
                    self.peer_id.encode('utf-8'),  # Peer ID
                    0,  # Downloaded
                    0,  # Left
                    0,  # Uploaded
                    1 if first else 0,  # Event (0表示无事件,1 started)
                    0,  # IP address (0表示默认)
                    0,  # key
                    -1,  # num want -1 default
                    random.randint(6000, 18888)  # Port
                )
                self.sock.sendto(announce_request)
                datagram, remote_addr = await self.sock.recvfrom()  # 收到peers的相关信息
                action, transaction_id, interval, leechers, seeders = struct.unpack('>IIIII', datagram[:20])
                peer_info_len = int((len(datagram) - 20) / 6)
                all_peers = []  # 所有peers的相关信息
                for i in range(0, peer_info_len):  # 得到所有的peers的ip,port
                    data = datagram[20 + i * 6: 20 + (i + 1) * 6]
                    ip, port = struct.unpack('>IH', data)
                    ip_addr = int_to_IP(ip)
                    all_peers.append([ip_addr, port])

                dict_data = {b"action": action, b"transaction_id": transaction_id, b"interval": interval,
                             b"leechers": leechers,
                             b"seeders": seeders, b"peers": datagram[20:]}
                return TrackerResponse(dict_data, True)
            except Exception as e:
                logging.info(f"Unable to connect to udp tracker:{self.announce, e}")
                self.can_connect = False
        else:  # 使用http协议的tracker
            if self.http_client is None:
                self.http_client = aiohttp.ClientSession()
            params = {
                'info_hash': self.torrent.info_hash,  # 文件的infohash
                'peer_id': self.peer_id,  # peer_id
                'port': 6881,  # 端口
                'uploaded': uploaded,
                'downloaded': downloaded,
                'left': self.torrent.length - downloaded,  # 剩余的字节数
                'compact': 1
            }
            if first:  # 第一次连接
                params['event'] = 'started'
            url = self.announce + "?" + urllib.parse.urlencode(params)
            logging.info('Connecting to tracker at: ' + url)
            try:
                async with self.http_client.get(url) as resp:
                    if not resp.status == 200:
                        raise ConnectionError('Unable to connect to tracker')
                    data = await resp.read()  # bencoded dictionary
                    return TrackerResponse(bencoding.Decode(data).decode(), False)
            except (aiohttp.ClientConnectorError, aiohttp.ClientOSError, aiohttp.ServerDisconnectedError):
                logging.info('Connect to tracker timeout!')
                self.can_connect = False

    async def close(self) -> None:
        """
        关闭掉异步资源
        """
        if self.use_udp:
            self.sock.close()
        else:
            await self.http_client.close()
