import logging
import re


class magnetLink:
    """
    magnetlink封装类，保存info_hash，display_name，trackers
    """

    def __init__(self, link, info_hash, display_name, trackers):
        self.link = link
        self.info_hash = info_hash
        self.display_name = display_name
        self.trackers = trackers

    def read_from_file(self, file_path: str):
        f = open(file_path, "r")
        meta_info = f.read()
        parsed_link = magnetlinkParser(meta_info).parse_magnetlink()
        self.link = parsed_link.link
        self.info_hash = parsed_link.info_hash
        self.display_name = parsed_link.display_name
        self.trackers = parsed_link.trackers

    def generate_mag_link(self):
        mag_link = "magnet:?xt=urn:btih:"
        mag_link += str(self.info_hash)
        mag_link += ("&dn=" + str(self.display_name))
        for tracker in self.trackers:
            mag_link += "&tr="
            mag_link += tracker
        logging.info("Generate magnet link file successfully!")
        return mag_link


class magnetlinkParser:
    """
    解析磁力链接，保存为magnetlink实例
    """
    magnetlink = ""

    def __init__(self, magnetlink):
        self.magnetlink = magnetlink

    def parse_magnetlink(self):
        info_hash = ""
        display_name = ""
        trackers = []

        # magnetlink对应的regex
        pattern = r"magnet:\?xt=urn:btih:([^&]+)(?:&dn=([^&]+))?(?:&tr=([^&]+(?:&tr=[^&]+)*))?"

        match = re.match(pattern, self.magnetlink)
        if match:
            info_hash = match.group(1)
            display_name = match.group(2) if match.group(2) else ""
            trackers = match.group(3).split("&tr=") if match.group(3) else []

        return magnetLink(link=self.magnetlink, info_hash=info_hash, display_name=display_name, trackers=trackers)
