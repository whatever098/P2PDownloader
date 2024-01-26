from urllib.parse import unquote

import requests

from src.magnetlink.MagnetlinkParser import magnetlinkParser


def get_torrent(url, file_path):
    """
    :param url: Request url
    :param file_path: 保存的文件地址
    :return: none
    """
    response = requests.get(url)
    print("Converting...")
    if response.status_code == 200:
        output_file = file_path + '/' + response.headers['Torrent-Name'] + '.torrent'
        decoded_text = unquote(output_file)
        with open(decoded_text, "wb") as f:
            f.write(response.content)
        print("Torrent file saved to", decoded_text)
    elif response.status_code == 504:
        print("Overtime, Maybe this magnetlink cannot convert to torrent!")
    else:
        print("Failed to retrieve the torrent file. HTTP status code:", response.status_code)


def magnet2torrent(magnetlink: str, file_path: str):
    """
    通过HTTP Request请求，得到返回的Torrent文件
    :param magnetlink: 磁力链接字符串
    :param file_path: 保存的文件地址
    :return:
    """
    parsed_link = magnetlinkParser(magnetlink=magnetlink).parse_magnetlink()
    url = "https://m2t.lolicon.app/m/" + parsed_link.info_hash
    get_torrent(url, file_path)
