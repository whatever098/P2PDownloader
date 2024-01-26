from MagnetlinkParser import magnetLink
from ..torrent.torrent import Torrent


class torrentToMagnetlink:
    def __init__(self, filepath: str):
        torrent = Torrent(filepath)
        self.info_hash = torrent.info_hash
        self.file_name = torrent.meta_info['name']
        self.file_comment = torrent.meta_info['comment']
        self.trackers = torrent.meta_info['announce']

    """
    首先使用torrent文件进行init，再调用该函数得到磁力链接
    """

    def get_magnetlink_link(self):
        link = magnetLink(link="", info_hash=self.info_hash, display_name=self.file_name, trackers=self.trackers)
        mag_link = link.generate_mag_link()
        return mag_link
