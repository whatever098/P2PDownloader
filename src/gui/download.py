import asyncio
import logging
import signal
from asyncio import CancelledError

from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent


def download(torrentfile: str):
    """
    下载开始接口，在实现图形化界面时可多次调用，建议设置过最大同时下载数为3
    :param torrentfile: .Torrent文件路径
    :return:
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%Y/%m/%d %I:%M:%S %p')
    loop = asyncio.get_event_loop()
    client = TorrentClient(Torrent(torrentfile))
    task = loop.create_task(client.start())

    def signal_handler(*_):
        logging.info('Exiting, please wait until everything is shutdown...')
        client.stop()
        task.cancel()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        loop.run_until_complete(task)
    except CancelledError:
        logging.warning('Event loop was canceled')

