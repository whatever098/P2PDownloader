from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton,
                               QVBoxLayout)


class Ui_Capture(object):
    """
    网页捕获音视频的UI界面
    """

    def setupUi(self, Capture):
        if not Capture.objectName():
            Capture.setObjectName(u"Capture")
        Capture.resize(351, 261)

        # 设置窗口图标为Beholder
        icon = QIcon()
        icon.addFile(u"resource/logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        Capture.setWindowIcon(icon)

        # 创建垂直布局，用于安排界面元素的垂直排列
        self.verticalLayout = QVBoxLayout(Capture)
        self.verticalLayout.setObjectName(u"verticalLayout")

        # 创建标题标签
        self.label_2 = QLabel(Capture)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font.setPointSize(26)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setIndent(-1)

        self.verticalLayout.addWidget(self.label_2)  # 将标题标签添加到布局中

        # 创建标签用于显示提示消息
        self.label = QLabel(Capture)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"\u534e\u6587\u6977\u4f53"])
        font1.setPointSize(12)
        self.label.setFont(font1)

        self.verticalLayout.addWidget(self.label)

        # 创建文本框，用于输入捕获的网址
        self.lineEdit = QLineEdit(Capture)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lineEdit)

        # 创建标签，用于显示“下载地址”字样
        self.label_3 = QLabel(Capture)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.verticalLayout.addWidget(self.label_3)

        # 创建按钮，用于选择下载路径
        self.pushButton_path = QPushButton(Capture)
        self.pushButton_path.setObjectName(u"pushButton_path")

        self.verticalLayout.addWidget(self.pushButton_path)

        # 创建按钮，用于开始捕获操作
        self.pushButton = QPushButton(Capture)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Capture)  # 设置UI元素的文本内容

        QMetaObject.connectSlotsByName(Capture)  # 连接信号和槽

    def retranslateUi(self, Capture):
        Capture.setWindowTitle(QCoreApplication.translate("Capture", u"Capture", None))
        self.label_2.setText(QCoreApplication.translate("Capture", u"\u7f51\u9875\u6355\u83b7\u97f3\u89c6\u9891", None))
        self.label.setText(QCoreApplication.translate("Capture", u"\u7f51\u5740\uff1a", None))
        self.lineEdit.setPlaceholderText(
            QCoreApplication.translate("Capture", u"\u8bf7\u8f93\u5165\u60f3\u8981\u6355\u83b7\u7684\u7f51\u5740",
                                       None))
        self.label_3.setText(QCoreApplication.translate("Capture", u"\u4e0b\u8f7d\u5730\u5740\uff1a", None))
        self.pushButton_path.setText(
            QCoreApplication.translate("Capture", u"\u9009\u62e9\u4e0b\u8f7d\u5730\u5740", None))
        self.pushButton.setText(QCoreApplication.translate("Capture", u"\u5f00\u59cb\u6355\u83b7", None))
