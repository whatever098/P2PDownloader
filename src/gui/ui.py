import asyncio
import logging
import signal
import sys
from asyncio import CancelledError

from PySide6.QtCore import QThread, Signal, QObject, Slot
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog

from src.gui.Capture import Ui_Capture
from src.gui.m3u8 import Ui_m3u8
from src.gui.magnetlink import Ui_magnetlink
from src.gui.mainwindow import Ui_MainWindow
from src.gui.small_capture import Ui_small_capture
from src.gui.torrent import Ui_torrent
from src.m3u8.m3u8 import interface_ui
from src.magnetlink.MagnetlinkToTorrent import magnet2torrent
from src.movie.videoplayer import MainWindow
from src.torrent.client import TorrentClient
from src.torrent.torrent import Torrent
from src.videos_audios_capture.capture import capture


class StreamRedirect(QObject):
    new_output = Signal(str)

    def __init__(self):
        super().__init__()

    def write(self, text):
        self.new_output.emit(text)


# 创建一个自定义的 StreamHandler
class QTextEditStreamHandler(logging.Handler):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        log_message = self.format(record)
        self.text_edit.insertPlainText(log_message)


class m3u8_thread(QThread):
    log_signal = Signal(str)

    def __init__(self, url, path, name):
        super().__init__()
        self.url = url
        self.path = path
        self.name = name

    def run(self):
        interface_ui(self.url, self.path, self.name)
        # 通知主线程处理完成
        self.log_signal.emit("m3u8_thread finished.\n")


class magnetlink_thread(QThread):
    log_signal = Signal(str)

    def __init__(self, url, path):
        super().__init__()
        self.url = url
        self.path = path

    def run(self):
        magnet2torrent(self.url, self.path)
        # 通知主线程处理完成
        self.log_signal.emit("m3u8_thread finished.\n")


class torrent_tread_start(QThread):
    signal_speed = Signal(float)
    signal_progress = Signal(float)
    signal_done = Signal(bool)

    def __init__(self, file, path):
        super().__init__()
        self.file = file
        self.path = path
        self.client = TorrentClient(Torrent(self.file))

    async def speed(self, client):
        while not client.piece_manager.finished:
            self.signal_speed.emit(client.download_speed)
            await asyncio.sleep(1)
        self.signal_speed.emit(0)
        client.stop()

    async def progress(self, client):
        while not client.piece_manager.finished:
            self.signal_progress.emit(client.download_Progress)
            await asyncio.sleep(1)
        self.signal_progress.emit(100)
        client.stop()

    def restart_(self):
        # 重新开始下载
        self.client.restart()

    def pause_(self):
        # 暂停下载
        self.client.pause()

    def stop_(self):
        # 停止下载
        self.client.stop()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.client = TorrentClient(Torrent(self.file))
        self.client.find_download_place(self.path)
        task = loop.create_task(self.client.start())
        task2 = loop.create_task(self.client.return_download_time())
        task3 = loop.create_task(self.client.download_progress())
        task4 = loop.create_task(self.speed(self.client))
        task5 = loop.create_task(self.progress(self.client))

        def signal_handler(*_):
            logging.info('Exiting, please wait until everything is shutdown...')
            self.client.stop()
            task.cancel()

            signal.signal(signal.SIGINT, signal_handler)

        try:
            loop.run_until_complete(task)
            loop.run_until_complete(task2)
            loop.run_until_complete(task3)
            loop.run_until_complete(task4)
            loop.run_until_complete(task5)
        except CancelledError:
            logging.warning('Event loop was canceled')


class magnetlink_ui(QWidget, Ui_magnetlink):
    def __init__(self):
        super().__init__()
        self.ui = Ui_magnetlink()
        self.ui.setupUi(self)
        self.ui.file_path_btn.clicked.connect(self.select_path)
        self.ui.confirm_btn.clicked.connect(self.start_magnetlink)
        self.worker = None

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.file_path_btn.setText(path)

    def start_magnetlink(self):
        magnetlink = self.ui.magnetlink_str.text()
        path = self.ui.file_path_btn.text()
        self.worker = magnetlink_thread(magnetlink, path)
        self.worker.start()

        stream_redirect.new_output.connect(self.receive_output_mag)

    # 新的槽方法，用于追加输出到QTextEdit
    @Slot(str)
    def receive_output_mag(self, text):
        self.ui.textBrowser.append(text)


class m3u8_ui(QWidget, Ui_m3u8):
    def __init__(self):
        super().__init__()
        self.ui = Ui_m3u8()
        self.ui.setupUi(self)
        self.ui.pushButton_path.clicked.connect(self.select_path)
        self.ui.pushButton.clicked.connect(self.start_m3u8)
        self.worker = None

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start_m3u8(self):
        url = self.ui.lineEdit_m3u8.text()
        path = self.ui.pushButton_path.text()
        name = self.ui.lineEdit_name.text()
        self.worker = m3u8_thread(url, path, name)
        self.worker.start()

        stream_redirect.new_output.connect(self.receive_output)

    # 新的槽方法，用于追加输出到QTextEdit
    @Slot(str)
    def receive_output(self, text):
        self.ui.log_text_browser.append(text)


class small_capture_ui(QWidget, Ui_small_capture):
    def __init__(self):
        super().__init__()
        self.ui = Ui_small_capture()
        self.ui.setupUi(self)
        # self.ui.label.setText("下载失败")


class capture_thread(QThread):
    log_signal = Signal(bool)

    def __init__(self, url, path):
        super().__init__()
        self.url = url
        self.path = path

    def run(self):
        result = capture(self.url, self.path)
        # 通知主线程处理完成
        self.log_signal.emit(result)


class capture_ui(QWidget, Ui_Capture):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Capture()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_capture)
        self.ui.pushButton_path.clicked.connect(self.select_path)
        self.worker = None

    def select_path(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start_capture(self):
        url = self.ui.lineEdit.text()
        path = self.ui.pushButton_path.text()
        self.worker = capture_thread(url, path)
        self.worker.start()
        self.ui.pushButton.setText("捕获完成！")


class torrent_ui(QWidget, Ui_torrent):
    def __init__(self):
        super().__init__()
        self.ui = Ui_torrent()
        self.ui.setupUi(self)
        self.ui.label_2.setText("下载速度：")
        self.ui.pushButton.clicked.connect(self.open_torrent_file_dialog)
        self.ui.pushButton_path.clicked.connect(self.download_place)
        self.ui.pushButton_pause.clicked.connect(self.pause)
        self.ui.pushButton_restart.clicked.connect(self.restart)
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_stop.clicked.connect(self.stop)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setFormat("{:.1f}%".format(0.0))
        self.thread_ = None

    def open_torrent_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Torrent Files (*.torrent)")  # 设置文件过滤器，只允许选择.torrent文件
        file_dialog.setViewMode(QFileDialog.List)
        torrent_file, _ = file_dialog.getOpenFileName(self, "选择 .torrent 文件", "", "Torrent Files (*.torrent)")
        self.ui.pushButton.setText(torrent_file)

    def download_place(self):
        path = QFileDialog.getExistingDirectory(self)
        self.ui.pushButton_path.setText(path)

    def start(self):
        self.thread_ = torrent_tread_start(self.ui.pushButton.text(), self.ui.pushButton_path.text())
        self.thread_.signal_progress.connect(self.callback_progress)
        self.thread_.signal_speed.connect(self.callback_speed)
        self.thread_.start()

    def callback_progress(self, result):
        self.ui.progressBar.setValue(result)
        self.ui.progressBar.setFormat("{:.1f}%".format(result))

    def callback_speed(self, result):
        self.ui.label_2.setText(f"下载速度：{result:.2f} KB/S")

    def restart(self):
        self.thread_.restart_()

    def pause(self):
        self.thread_.pause_()

    def stop(self):
        self.thread_.stop_()
        self.close()


class main_ui(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.torrent_button)
        self.ui.pushButton_mp3.clicked.connect(self.mp3_button)
        self.ui.pushButton_reptiles.clicked.connect(self.capture_button)
        self.ui.pushButton_m3u8.clicked.connect(self.m3u8_button)
        self.ui.pushButton_magnetlink.clicked.connect(self.magnetlink_button)

    def m3u8_button(self):
        self.ui = m3u8_ui()
        self.ui.show()

    def magnetlink_button(self):
        self.ui = magnetlink_ui()
        self.ui.show()

    def torrent_button(self):
        self.ui = torrent_ui()
        self.ui.show()

    def mp3_button(self):
        self.ui = MainWindow()
        self.ui.show()

    def capture_button(self):
        self.ui = capture_ui()
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stream_redirect = StreamRedirect()
    sys.stdout = stream_redirect
    window = main_ui()
    window.show()
    app.exec()
