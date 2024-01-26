# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'm3u8.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QGridLayout, QLabel, QLineEdit,
                               QPushButton, QTextBrowser)


class Ui_m3u8(object):
    def setupUi(self, m3u8):
        if not m3u8.objectName():
            m3u8.setObjectName(u"m3u8")
        self.width = 800
        self.height = 600
        m3u8.resize(self.width, self.height)
        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        m3u8.setWindowIcon(icon)
        self.gridLayout = QGridLayout(m3u8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(m3u8)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 11, 0, 1, 1)

        self.lineEdit_name = QLineEdit(m3u8)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        self.lineEdit_name.setBaseSize(QSize(0, 20))
        self.lineEdit_name.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_name, 10, 0, 1, 1)

        self.lineEdit_m3u8 = QLineEdit(m3u8)
        self.lineEdit_m3u8.setObjectName(u"lineEdit_m3u8")
        self.lineEdit_m3u8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_m3u8, 4, 0, 1, 1)

        self.pushButton_path = QPushButton(m3u8)
        self.pushButton_path.setObjectName(u"pushButton_path")

        self.gridLayout.addWidget(self.pushButton_path, 8, 0, 1, 1)

        self.label_3 = QLabel(m3u8)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.label_2 = QLabel(m3u8)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.label_4 = QLabel(m3u8)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 9, 0, 1, 1)

        self.label = QLabel(m3u8)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        # 创建一个 QTextBrowser 用于显示日志信息
        self.log_text_browser = QTextBrowser()
        self.log_text_browser.setReadOnly(True)

        font_out = QFont()
        font_out.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font_out.setPointSize(12)
        self.log_text_browser.setFont(font_out)
        self.log_text_browser.setLineWidth(15)

        # 设置样式表
        self.log_text_browser.setStyleSheet("QTextBrowser { line-height: normal; }")
        # 将 QTextBrowser 添加到 UI 窗口的布局中
        self.gridLayout.addWidget(self.log_text_browser)

        self.retranslateUi(m3u8)

        QMetaObject.connectSlotsByName(m3u8)

    def retranslateUi(self, m3u8):
        m3u8.setWindowTitle(QCoreApplication.translate("m3u8", u"m3u8", None))
        self.pushButton.setText(QCoreApplication.translate("m3u8", u"\u786e\u8ba4\u4e0b\u8f7d", None))
        self.lineEdit_name.setPlaceholderText(
            QCoreApplication.translate("m3u8", u"\u8bf7\u8f93\u5165\u4fdd\u5b58\u7684\u6587\u4ef6\u540d", None))
        self.lineEdit_m3u8.setPlaceholderText(
            QCoreApplication.translate("m3u8", u"\u8bf7\u8f93\u5165m3u8\u7f51\u5740", None))
        self.pushButton_path.setText(QCoreApplication.translate("m3u8", u"\u9009\u62e9\u4e0b\u8f7d\u8def\u5f84", None))
        self.label_3.setText(QCoreApplication.translate("m3u8", u"\u4e0b\u8f7d\u8def\u5f84\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("m3u8", u"m3u8\u8bf7\u6c42url\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("m3u8", u"\u4fdd\u5b58\u6587\u4ef6\u540d\uff1a", None))
        self.label.setText(QCoreApplication.translate("m3u8", u"m3u8\u4e0b\u8f7d\u5668", None))
