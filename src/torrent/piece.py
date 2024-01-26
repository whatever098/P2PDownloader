import logging
import time
from hashlib import sha1
from typing import Optional

"""
    @filename piece.py
    @author 郑卯杨
    @date 2023/10/10
    @version 1.0
    
    该模块定义了与Peer通信时用到的数据结构Block和Piece
    Block: 向Peer请求数据的最小单位
    Piece: Torrent文件被划分的最小单位
"""


class Block:
    """
    Block是Piece的一部分,每次向Peer请求的是Block大小的数据
    除了每个Piece的最后一个Block外,每一个Block都是REQUEST_SIZE(2**14)
    """
    Missing = 0
    Pending = 1
    Retrieved = 2

    def __init__(self, piece: int, offset: int, length: int):
        """
        :param piece: 属于哪一个piece
        :param offset: 在piece中的偏移
        :param length: 数据长度
        """
        self.piece = piece
        self.offset = offset
        self.length = length
        self.status = Block.Missing
        self.time = None
        self.data = None


class Piece:
    """
    Piece是Torrent文件被划分的最小单位,通过Piece来管理Block
    """
    def __init__(self, index: int, blocks: [], hash_value):
        """
        :param index: 在整个文件中的index
        :param blocks: 被划分的所有block
        :param hash_value: 所有数据一起使用sha1计算出的hash,用于核对信息
        """
        self.index = index
        self.blocks = blocks
        self.hash = hash_value

    def reset(self) -> None:
        """
        将Piece里的所有块的状态都重置为Missing
        """
        for block in self.blocks:
            block.status = Block.Missing

    def next_request(self) -> Optional[Block]:
        """
        :return: 返回第一个缺失的Block
        """
        missing = [b for b in self.blocks if b.status is Block.Missing]
        if missing:
            missing[0].status = Block.Pending
            return missing[0]
        pending = [b for b in self.blocks if b.status is Block.Pending]  # debug：防止有些pending blocks卡在队列里
        cur_time = round(time.time())
        if pending and cur_time - pending[0].time > 60:
            pending[0].status = Block.Pending
            return pending[0]
        return None

    def block_received(self, offset: int, data: bytes):
        """接受对应的Block数据

        :param offset: Block在Piece中的偏移量
        :param data: 接受到的Block的数据
        """
        match = [b for b in self.blocks if b.offset == offset]
        block = match[0] if match else None
        if block:
            block.status = Block.Retrieved
            block.data = data
        else:
            logging.warning(f"Trying to receive a non-existing block {offset=}")

    def finished(self) -> bool:
        """
        :return: 是否已经接受该Piece的所有Block
        """
        blocks = [b for b in self.blocks if b.status is not Block.Retrieved]
        return len(blocks) == 0

    @property
    def data(self) -> bytes:
        """
        :return:将所有Block的数据按序合并
        """
        total = sorted(self.blocks, key=lambda b: b.offset)
        return b''.join([b.data for b in total])

    def match(self) -> bool:
        """
        :return: 是否hash匹配
        """
        piece_hash = sha1(self.data).digest()
        return piece_hash == self.hash
