# @author 郑卯杨
# @date 2023/9/24
# @description 测试bencoding模块的正确性

import unittest

from src.torrent.bencoding import *


class TestDecode(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(Decode(b'i1234e').decode(), 1234)

    def test_string(self):
        self.assertEqual(Decode(b'4:spam').decode(), b'spam')
        self.assertEqual(Decode(b'0:').decode(), b'')

    def test_list(self):
        self.assertEqual(Decode(b'l4:spam4:eggse').decode(), [b'spam', b'eggs'])
        self.assertEqual(Decode(b'le').decode(), [])

    def test_dict(self):
        self.assertEqual(Decode(b'd3:cow3:moo4:spam4:eggse').decode(),
                         OrderedDict({b'cow': b'moo', b'spam': b'eggs'}))

        self.assertEqual(Decode(b'd4:spaml1:a1:bee').decode(),
                         OrderedDict({b'spam': [b'a', b'b']}))

        self.assertEqual(
            Decode(b'd9:publisher3:bob17:publisher-webpage15:www.example.com18:publisher.location4:homee').decode(),
            OrderedDict(
                {b'publisher': b'bob', b'publisher-webpage': b'www.example.com', b'publisher.location': b'home'}))


class TestEncode(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(b'i1234e', Encode(1234).encode())

    def test_string(self):
        self.assertEqual(b'4:spam', Encode('spam').encode())
        self.assertEqual(b'0:', Encode('').encode())

    def test_list(self):
        self.assertEqual(b'l4:spam4:eggse', Encode(['spam', 'eggs']).encode())
        self.assertEqual(b'le', Encode([]).encode())

    def test_dict(self):
        self.assertEqual(b'd3:cow3:moo4:spam4:eggse',
                         Encode(OrderedDict({'cow': 'moo', 'spam': 'eggs'})).encode())

        self.assertEqual(b'd4:spaml1:a1:bee',
                         Encode(OrderedDict({'spam': ['a', 'b']})).encode())

        self.assertEqual(
            b'd9:publisher3:bob17:publisher-webpage15:www.example.com18:publisher.location4:homee',
            Encode(OrderedDict(
                {'publisher': 'bob', 'publisher-webpage': 'www.example.com',
                 'publisher.location': 'home'})).encode())


if __name__ == '__main__':
    unittest.main()
