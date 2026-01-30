  # -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(740, 640)
        self.HousingSystemTitle = QLabel(Dialog)
        self.HousingSystemTitle.setObjectName(u"HousingSystemTitle")
        self.HousingSystemTitle.setGeometry(QRect(250, 80, 211, 61))
        font = QFont()
        font.setFamilies([u"LiHei Pro"])
        font.setPointSize(23)
        self.HousingSystemTitle.setFont(font)
        self.HousingSystemTitle.setStyleSheet(u"background-color: rgb(121, 121, 121);")
        self.Login_Button = QPushButton(Dialog)
        self.Login_Button.setObjectName(u"Login_Button")
        self.Login_Button.setGeometry(QRect(260, 240, 201, 41))
        self.Login_Button.setStyleSheet(u"background-color: rgb(122, 122, 122);")
        self.PassWord = QLineEdit(Dialog)
        self.PassWord.setObjectName(u"PassWord")
        self.PassWord.setGeometry(QRect(260, 180, 201, 41))
        self.PassWord_Title = QLabel(Dialog)
        self.PassWord_Title.setObjectName(u"PassWord_Title")
        self.PassWord_Title.setGeometry(QRect(170, 190, 81, 21))
        self.PassWord_Title.setStyleSheet(u"background-color: rgb(132, 131, 124);")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.HousingSystemTitle.setText(QCoreApplication.translate("Dialog", u"HOUSING SYSTEM", None))
        self.Login_Button.setText(QCoreApplication.translate("Dialog", u"LOGIN", None))
        self.PassWord_Title.setText(QCoreApplication.translate("Dialog", u"PASSWORD:", None))
    # retranslateUi



