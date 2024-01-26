import sys
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Slot
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtMultimedia import QMediaFormat


class MyAudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()  # 不能实例化为临时变量，否则被自动回收导致无法播放
        self.player.setAudioOutput(self.audioOutput)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.playbackStateChanged.connect(self.stateChanged)
        self.player.errorOccurred.connect(self._player_error)
        # Qt6中`QMediaPlayer.setVolume`已被移除，使用`QAudioOutput.setVolume`替代
        self.audioOutput.setVolume(1)

    @Slot()
    def positionChanged(self, position):
        print(f'positionChanged: {position}')

    @Slot()
    def durationChanged(self, duration):
        print(f'durationChanged: {duration}')

    @Slot()
    def stateChanged(self, state):
        print(f'stateChanged: {state}')

    @Slot()
    def _player_error(self, error, error_string):
        print(error, error_string)

    def play(self, file_path):
        fp = file_path
        # `QMediaPlayer.setMedia` 方法已从Qt6中移除，使用`.setSource`
        self.player.setSource(QUrl.fromLocalFile(fp))
        self.player.play()


def get_supported_mime_types():
    """
    这个方法需耗时几秒钟
    """
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


if __name__ == '__main__':
    # print(get_supported_mime_types())
    file = "mp3"
    app = QApplication(sys.argv)
    audioPlayer = MyAudioPlayer()
    audioPlayer.show()
    audioPlayer.play(file_path=file)
    sys.exit(app.exec())
