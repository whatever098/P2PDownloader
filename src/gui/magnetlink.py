from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QGridLayout, QLabel, QLineEdit,
                               QPushButton, QSizePolicy, QTextBrowser)


class Ui_magnetlink(object):
    def setupUi(self, magnetlink):
        if not magnetlink.objectName():
            magnetlink.setObjectName(u"magnetlink")
        magnetlink.resize(830, 636)

        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        magnetlink.setWindowIcon(icon)
        self.gridLayout = QGridLayout(magnetlink)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(magnetlink)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.textBrowser = QTextBrowser()
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setObjectName(u"textBrowser")

        font_out = QFont()
        font_out.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font_out.setPointSize(12)

        self.textBrowser.setFont(font_out)
        self.textBrowser.setLineWidth(15)
        self.textBrowser.setStyleSheet("QTextBrowser { line-height: normal; }")

        self.gridLayout.addWidget(self.textBrowser, 6, 0, 1, 1)

        self.file_path_btn = QPushButton(magnetlink)
        self.file_path_btn.setObjectName(u"file_path_btn")

        self.gridLayout.addWidget(self.file_path_btn, 4, 0, 1, 1)

        self.confirm_btn = QPushButton(magnetlink)
        self.confirm_btn.setObjectName(u"confirm_btn")

        self.gridLayout.addWidget(self.confirm_btn, 5, 0, 1, 1)

        self.magnetlink_str = QLineEdit(magnetlink)
        self.magnetlink_str.setObjectName(u"magnetlink_str")
        self.magnetlink_str.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.magnetlink_str, 3, 0, 1, 1)

        self.retranslateUi(magnetlink)

        QMetaObject.connectSlotsByName(magnetlink)

    # setupUi

    def retranslateUi(self, magnetlink):
        magnetlink.setWindowTitle(QCoreApplication.translate("magnetlink", u"Form", None))
        self.label.setText(
            QCoreApplication.translate("magnetlink", u"\u78c1\u529b\u94fe\u63a5\u8f6ctorrent\u6587\u4ef6", None))
        self.file_path_btn.setText(
            QCoreApplication.translate("magnetlink", u"\u9009\u62e9\u4e0b\u8f7d\u8def\u5f84", None))
        self.confirm_btn.setText(QCoreApplication.translate("magnetlink", u"\u786e\u8ba4\u8f6c\u6362", None))
        self.magnetlink_str.setWhatsThis(
            QCoreApplication.translate("magnetlink", u"\u8f93\u5165\u78c1\u529b\u94fe\u63a5", None))
        self.magnetlink_str.setPlaceholderText(
            QCoreApplication.translate("magnetlink", u"\u8f93\u5165\u78c1\u529b\u94fe\u63a5", None))
