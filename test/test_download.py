import asyncio
import logging
import signal
from asyncio import CancelledError
from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%Y/%m/%d %I:%M:%S %p')
    client = TorrentClient(Torrent("file/debian-12.1.0-amd64-netinst.iso.torrent"))
    loop = asyncio.get_event_loop()
    task = loop.create_task(client.start())
    task2 = loop.create_task(client.return_download_time())

    # Pause after 20 seconds
    await asyncio.sleep(20)
    client.pause()

    # Restart after 30 seconds
    # await asyncio.sleep(10)
    # client.restart()

    def signal_handler(*_):
        logging.info('Exiting, please wait until everything is shutdown...')
        client.stop()
        task.cancel()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        await task
        await task2
    except CancelledError:
        logging.warning('Event loop was canceled')


if __name__ == '__main__':
    asyncio.run(main())
