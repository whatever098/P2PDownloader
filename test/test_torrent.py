# @author 郑卯杨
# @date 2023/9/24
# @description 测试torrent模块的正确性

import unittest

from src.torrent.torrent import Torrent


class TestTorrent(unittest.TestCase):
    def test_parser(self):
        filepath = 'file/debian-12.1.0-amd64-netinst.iso.torrent'
        torrent_file = Torrent(filepath)
        self.assertEqual(torrent_file.announce, "http://bttracker.debian.org:6969/announce")
        self.assertEqual(torrent_file.length, 657457152)
        self.assertEqual(torrent_file.name, 'debian-12.1.0-amd64-netinst.iso')
        self.assertEqual(torrent_file.piece_length, 262144)
        self.assertEqual(len(torrent_file.pieces), torrent_file.length // torrent_file.piece_length)


if __name__ == '__main__':
    unittest.main()
