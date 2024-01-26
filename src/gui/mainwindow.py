from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QLabel, QPushButton, QVBoxLayout)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(510, 412)
        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(MainWindow)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setIndent(-1)

        self.verticalLayout.addWidget(self.label)

        self.pushButton = QPushButton(MainWindow)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_magnetlink = QPushButton(MainWindow)
        self.pushButton_magnetlink.setObjectName(u"pushButton_magnetlink")

        self.verticalLayout.addWidget(self.pushButton_magnetlink)

        self.pushButton_m3u8 = QPushButton(MainWindow)
        self.pushButton_m3u8.setObjectName(u"pushButton_m3u8")

        self.verticalLayout.addWidget(self.pushButton_m3u8)

        self.pushButton_reptiles = QPushButton(MainWindow)
        self.pushButton_reptiles.setObjectName(u"pushButton_reptiles")

        self.verticalLayout.addWidget(self.pushButton_reptiles)

        self.pushButton_mp3 = QPushButton(MainWindow)
        self.pushButton_mp3.setObjectName(u"pushButton_mp3")

        self.verticalLayout.addWidget(self.pushButton_mp3)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Beholder/BT Torrent Downloader", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"P2P\u4e0b\u8f7d\u5668", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Torrent\u6587\u4ef6\u4e0b\u8f7d", None))
        self.pushButton_magnetlink.setText(
            QCoreApplication.translate("MainWindow", u"\u78c1\u529b\u94fe\u63a5\u8f6cTorrent\u6587\u4ef6", None))
        self.pushButton_m3u8.setText(QCoreApplication.translate("MainWindow", u"M3U8\u89c6\u9891\u4e0b\u8f7d", None))
        self.pushButton_reptiles.setText(
            QCoreApplication.translate("MainWindow", u"\u7f51\u9875\u6355\u83b7\u97f3\u89c6\u9891", None))
        self.pushButton_mp3.setText(
            QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u64ad\u653e\u5668", None))
    # retranslateUi
