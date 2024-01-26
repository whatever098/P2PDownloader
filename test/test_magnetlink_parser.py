import unittest

from src.magnetlink.MagnetlinkParser import magnetlinkParser, magnetLink


class TestMagnetlink(unittest.TestCase):
    def test_parser(self):
        link_str = (
            "magnet:?xt=urn:btih:4225824a42f4afceec51cf73ae85fdc76f14aebd&dn=Mind.Games.rar&tr=udp%3a%2f%2ftracker"
            ".torrent"
            ".eu.org%3a451%2fannounce&tr=udp%3a%2f%2fexodus.desync.com%3a6969%2fannounce&tr=udp%3a%2f%2ftracker"
            ".moeking.me"
            "%3a6969%2fannounce")
        link_to_parse = magnetlinkParser(link_str).parse_magnetlink()

        trackers = ['udp%3a%2f%2ftracker.torrent.eu.org%3a451%2fannounce',
                    'udp%3a%2f%2fexodus.desync.com%3a6969%2fannounce',
                    'udp%3a%2f%2ftracker.moeking.me%3a6969%2fannounce']
        self.assertEqual(link_to_parse.info_hash, "4225824a42f4afceec51cf73ae85fdc76f14aebd")
        self.assertEqual(link_to_parse.trackers, trackers)
        self.assertEqual(link_to_parse.display_name, "Mind.Games.rar")
        link = magnetLink(link_str, link_to_parse.info_hash, link_to_parse.display_name, link_to_parse.trackers)
        mag_link = link.generate_mag_link()
        self.assertEqual(mag_link, link_str)


if __name__ == '__main__':
    unittest.main()
