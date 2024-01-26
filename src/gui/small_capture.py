from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QLabel, QVBoxLayout)


class Ui_small_capture(object):
    def setupUi(self, small_capture):
        if not small_capture.objectName():
            small_capture.setObjectName(u"small_capture")
        small_capture.resize(215, 138)
        self.verticalLayout = QVBoxLayout(small_capture)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(small_capture)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(small_capture)

        QMetaObject.connectSlotsByName(small_capture)

    # setupUi

    def retranslateUi(self, small_capture):
        small_capture.setWindowTitle(QCoreApplication.translate("small_capture", u"Form", None))
        self.label.setText(QCoreApplication.translate("small_capture", u"TextLabel", None))
    # retranslateUi
