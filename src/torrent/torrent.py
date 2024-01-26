import logging
from hashlib import sha1
from typing import List

from src.torrent import bencoding

"""
    @filename torrent.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0
    
    该模块对解析bencoding格式二进制文件后生成的OrderedDict进行了封装
    实现了封装类Torrent,通过torrent的属性访问
"""


class Torrent:
    def __init__(self, filepath: str):
        """
        :param filepath: 需要解析的.torrent文件路径
        :raise RuntimeError: 如果该torrent文件是多文件下载模式,抛出异常，停止本次下载
        """
        self.filepath = filepath
        with open(filepath, 'rb') as f:
            meta_info = f.read()  # bytes
            # OrderedDict，包括announce, announce-list, info(name, length, piece length, pieces)...
            self.meta_info = bencoding.Decode(meta_info).decode()  # 使用自己编写的bencoding模块解码
            # self.meta_info = bencodepy.decode(meta_info)

            # 由info进行bencode.encode得到infohash(bytes)
            info_hash = bencoding.Encode(self.meta_info[b'info']).encode()
            # 再由sha1加密算法得到infohash(string)
            self.info_hash: bytes = sha1(info_hash).digest()  # str size = 20
            self.info_bytes = info_hash
            logging.info(f"announce={self.meta_info[b'announce'].decode('utf-8')}")

    @property
    def announce(self) -> str:
        """
        :return: 返回Tracker服务器的announce
        """
        return self.meta_info[b'announce'].decode('utf-8')

    @property
    def length(self) -> int:
        """
        :return: 返回下载时下载文件的总大小
        """
        if b'info' in self.meta_info:
            info = self.meta_info[b'info']
            if b'files' in info:
                # 如果存在多文件信息
                total_length = 0
                for file_info in info[b'files']:
                    if b'length' in file_info:
                        total_length += file_info[b'length']
                return total_length
            elif b'length' in info:
                # 如果只有一个文件
                return info[b'length']
        return 0  # 无效的 .torrent 文件或没有文件信息

    @property
    def pieces(self) -> List[bytes]:
        """
        :return: 返回一个列表,列表的每一项是对应的piece使用sha1算法计算出的hash值
        """
        res = []
        offset = 0
        data = self.meta_info[b'info'][b'pieces']
        length = len(data)
        while offset < length:
            res.append(data[offset:offset + 20])
            offset += 20
        return res

    @property
    def piece_length(self) -> int:
        """
        :return: 返回每一个piece的length
        """
        return self.meta_info[b'info'][b'piece length']

    @property
    def name(self) -> str:
        """
        :return: 返回要下载的文件的名字
        """
        return self.get_name()

    def get_name(self) -> str:
        return self.meta_info[b'info'][b'name'].decode('utf-8')

    @property
    def trackers(self) -> List[str]:
        """
        返回torrent文件中包含的所有trackers信息（dict形式）
        """
        if b'announce-list' in self.meta_info:
            return [url.decode('utf-8') for tier in self.meta_info[b'announce-list'] for url in tier]
        elif b'announce' in self.meta_info:
            return [self.meta_info[b'announce'].decode('utf-8')]
        else:
            return []

    def is_multi_file(self) -> bool:
        """
        判断是否为多文件
        :return: true or false
        """
        return b'files' in self.meta_info[b'info']

    def get_files(self):
        """
        :return: 文件信息列表
        """
        if self.is_multi_file():
            files = self.meta_info[b'info'][b'files']
            file_list = []
            for file_info in files:
                path = [item.decode('utf-8') for item in file_info[b'path']]
                length = file_info[b'length']
                file_list.append({'path': path, 'length': length})
            return file_list
        else:
            return [{'path': [self.get_name()], 'length': self.length}]
