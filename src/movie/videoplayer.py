import sys
from PySide6.QtCore import QStandardPaths, Qt, Slot, QTime, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,
                               QMainWindow, QSlider, QStyle, QToolBar, QVBoxLayout, QLabel)
from PySide6.QtMultimedia import (QAudioOutput, QMediaFormat,
                                  QMediaPlayer)
from PySide6.QtMultimediaWidgets import QVideoWidget

"""
实现视频播放器的UI界面
"""

AVI = "video/x-msvideo"  # AVI，支持的视频格式


def get_supported_mime_types():
    """
    得到支持的视频格式
    :return: 视频格式
    """
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._playlist = []
        self._playlist_index = -1
        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self.setWindowTitle("视频播放器")

        self.resize(1024, 800)
        icon = QIcon()
        icon.addFile(u"../gui/resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self._player.errorOccurred.connect(self._player_error)

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)

        file_menu = self.menuBar().addMenu("&File")  # 文件菜单（用于打开文件）
        icon = QIcon.fromTheme("document-open")
        open_action = QAction(icon, "&Open...", self,
                              shortcut=QKeySequence.Open, triggered=self.open)
        file_menu.addAction(open_action)
        tool_bar.addAction(open_action)
        icon = QIcon.fromTheme("application-exit")
        exit_action = QAction(icon, "E&xit", self,
                              shortcut="Ctrl+Q", triggered=self.close)
        file_menu.addAction(exit_action)

        # 以下为播放，上一次，暂停，下一个，停止的bar
        play_menu = self.menuBar().addMenu("&Play")
        style = self.style()
        icon = QIcon.fromTheme("media-playback-start.png",
                               style.standardIcon(QStyle.SP_MediaPlay))
        self._play_action = tool_bar.addAction(icon, "Play")
        self._play_action.triggered.connect(self._player.play)
        play_menu.addAction(self._play_action)

        icon = QIcon.fromTheme("media-skip-backward-symbolic.svg",
                               style.standardIcon(QStyle.SP_MediaSkipBackward))
        self._previous_action = tool_bar.addAction(icon, "Previous")
        self._previous_action.triggered.connect(self.previous_clicked)
        play_menu.addAction(self._previous_action)

        icon = QIcon.fromTheme("media-playback-pause.png",
                               style.standardIcon(QStyle.SP_MediaPause))
        self._pause_action = tool_bar.addAction(icon, "Pause")
        self._pause_action.triggered.connect(self._player.pause)
        play_menu.addAction(self._pause_action)

        icon = QIcon.fromTheme("media-skip-forward-symbolic.svg",
                               style.standardIcon(QStyle.SP_MediaSkipForward))
        self._next_action = tool_bar.addAction(icon, "Next")
        self._next_action.triggered.connect(self.next_clicked)
        play_menu.addAction(self._next_action)

        icon = QIcon.fromTheme("media-playback-stop.png",
                               style.standardIcon(QStyle.SP_MediaStop))
        self._stop_action = tool_bar.addAction(icon, "Stop")
        self._stop_action.triggered.connect(self._ensure_stopped)
        play_menu.addAction(self._stop_action)

        # 用于音量调节的bar
        self._volume_slider = QSlider()
        self._volume_slider.setOrientation(Qt.Horizontal)
        self._volume_slider.setMinimum(0)
        self._volume_slider.setMaximum(100)
        available_width = self.screen().availableGeometry().width()
        self._volume_slider.setFixedWidth(available_width / 10)
        self._volume_slider.setValue(self._audio_output.volume())
        self._volume_slider.setTickInterval(10)
        self._volume_slider.setTickPosition(QSlider.TicksBelow)
        self._volume_slider.setToolTip("Volume")
        self._volume_slider.valueChanged.connect(self._audio_output.setVolume)
        tool_bar.addWidget(self._volume_slider)

        # 用于进度条的bar
        tool_bar_2 = QToolBar()
        self.addToolBar(Qt.BottomToolBarArea, tool_bar_2)

        self._progress_slider = QSlider()
        self._progress_slider.setOrientation(Qt.Horizontal)
        self._progress_slider.setToolTip("Progress bar")
        self._progress_slider.sliderMoved.connect(self.set_position)
        tool_bar_2.addWidget(self._progress_slider)

        # 创建时间显示标签
        self._time_label = QLabel()
        tool_bar_2.addWidget(self._time_label)

        self._video_widget = QVideoWidget()
        self.setCentralWidget(self._video_widget)
        self._player.playbackStateChanged.connect(self.update_buttons)
        self._player.setVideoOutput(self._video_widget)
        self._player.positionChanged.connect(self.update_progress_slider)

        self.update_buttons(self._player.playbackState())
        self._mime_types = []

    # 更新进度条
    def update_progress_slider(self, position):
        """
        用于更新视频进度条的显示
        """
        duration = self._player.duration()
        self._progress_slider.setMaximum(duration)
        self._progress_slider.setValue(position)

        # 更新时间显示
        current_time = QTime(0, 0)
        current_time = current_time.addMSecs(position)
        total_time = QTime(0, 0)
        total_time = total_time.addMSecs(duration)

        # 格式化时间为 "mm:ss" 格式
        time_format = "mm:ss"
        current_time_display = current_time.toString(time_format)
        total_time_display = total_time.toString(time_format)

        self._time_label.setText(f"{current_time_display}/{total_time_display}")

    # 设置播放位置
    @Slot(int)
    def set_position(self, position):
        """
        设置播放位置
        """
        self._player.setPosition(position)

    def closeEvent(self, event):
        """
        停止
        """
        self._ensure_stopped()
        event.accept()

    @Slot()
    def open(self):
        self._ensure_stopped()
        file_dialog = QFileDialog(self)

        is_windows = sys.platform == 'win32'
        if not self._mime_types:
            self._mime_types = get_supported_mime_types()
            if (is_windows and AVI not in self._mime_types):
                self._mime_types.append(AVI)

        file_dialog.setMimeTypeFilters(self._mime_types)

        movies_location = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_location)
        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._playlist.append(url)
            self._playlist_index = len(self._playlist) - 1
            self._player.setSource(url)
            self._player.play()

    @Slot()
    def _ensure_stopped(self):
        if self._player.playbackState() != QMediaPlayer.StoppedState:
            self._player.stop()

    @Slot()
    def previous_clicked(self):
        # Go to previous track if we are within the first 5 seconds of playback
        # Otherwise, seek to the beginning.
        if self._player.position() <= 5000 and self._playlist_index > 0:
            self._playlist_index -= 1
            self._playlist.previous()
            self._player.setSource(self._playlist[self._playlist_index])
        else:
            self._player.setPosition(0)

    @Slot()
    def next_clicked(self):
        if self._playlist_index < len(self._playlist) - 1:
            self._playlist_index += 1
            self._player.setSource(self._playlist[self._playlist_index])

    @Slot("QMediaPlayer::PlaybackState")
    def update_buttons(self, state):
        media_count = len(self._playlist)
        self._play_action.setEnabled(media_count > 0
                                     and state != QMediaPlayer.PlayingState)
        self._pause_action.setEnabled(state == QMediaPlayer.PlayingState)
        self._stop_action.setEnabled(state != QMediaPlayer.StoppedState)
        self._previous_action.setEnabled(self._player.position() > 0)
        self._next_action.setEnabled(media_count > 1)

    def show_status_message(self, message):
        self.statusBar().showMessage(message, 5000)

    @Slot("QMediaPlayer::Error", str)
    def _player_error(self, error, error_string):
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(available_geometry.width() / 3,
                    available_geometry.height() / 2)
    main_win.show()
    sys.exit(app.exec())
