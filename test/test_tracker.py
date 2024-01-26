import asyncio
from src.torrent.tracker import Tracker
from src.torrent.torrent import Torrent


async def test_connect():
    filepath = 'file/B3273F22E02EC398C9C2B18F60EEF8166C89FB70.torrent'
    # filepath = '../file/C19CA813C4825C7011DAED258D2E3DE3D67380A5.torrent'
    torrent_file = Torrent(filepath)
    bt_tracker = Tracker(torrent_file)
    await bt_tracker.connect(True)
    bt_tracker.close()
    # try:
    #     tracker_resp = await bt_tracker.connect(True)
    #     if tracker_resp:
    #         print(tracker_resp.failure)
    #         print(tracker_resp.complete)
    #         print(tracker_resp.interval)
    #         print(tracker_resp.peers)
    #         print("--------------------------------")
    # finally:
    #     bt_tracker.close()


if __name__ == '__main__':
    asyncio.run(test_connect())
