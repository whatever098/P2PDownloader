import asyncio
import logging
import signal
from asyncio import CancelledError

from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog

from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent


class TorrentFileSelectorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Torrent 文件选择器")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建选择.torrent文件按钮
        self.select_torrent_button = QPushButton("选择 .torrent 文件", self)
        self.select_torrent_button.clicked.connect(self.open_torrent_file_dialog)
        layout.addWidget(self.select_torrent_button)

        self.central_widget.setLayout(layout)

    def open_torrent_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Torrent Files (*.torrent)")  # 设置文件过滤器，只允许选择.torrent文件
        file_dialog.setViewMode(QFileDialog.List)
        torrent_file, _ = file_dialog.getOpenFileName(self, "选择 .torrent 文件", "", "Torrent Files (*.torrent)")

        if torrent_file:
            logging.basicConfig(level=logging.INFO)
            loop = asyncio.get_event_loop()
            client = TorrentClient(Torrent(torrent_file))
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
