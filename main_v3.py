from PyQt5 import QtWidgets, QtGui, QtCore
import smtplib
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QScrollArea, QLineEdit, QHBoxLayout, QFrame, QFileDialog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import sqlite3
import qrcode
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QDate, QTime, QDir
import logging
from email.mime.image import MIMEImage
import os
import datetime
from user_reg_page import user_reg
from user_login_page import user_login
from business_login import Business_Login_Page

"""
color palette
#F5F7F7
#edb518
#79031D
#000407
"""

class landing_Page(object):
    def go_to_user_reg(self):
        self.ui = user_reg(MainWindow)
    def user_login(self):
        self.ui = user_login(MainWindow)
    def busin_login(self):
        self.ui = Business_Login_Page(MainWindow)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Landing_Page")
        MainWindow.resize(306, 479)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_page = QtWidgets.QLabel(self.centralwidget)
        self.main_page.setGeometry(QtCore.QRect(0, 0, 290, 410))
        self.main_page.setStyleSheet("background-color:#79031D;\n"
"border-radius: 10px")
        self.main_page.setText("")
        self.main_page.setObjectName("main_page")
        self.user_login_button = QtWidgets.QPushButton(self.centralwidget)
        self.user_login_button.setGeometry(QtCore.QRect(20, 230, 116, 28))
        self.user_login_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.user_login_button.setObjectName("user_login_button")
        self.buiss_login_button = QtWidgets.QPushButton(self.centralwidget)
        self.buiss_login_button.setGeometry(QtCore.QRect(20, 270, 235, 28))
        self.buiss_login_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.buiss_login_button.setObjectName("buiss_login_button")
        self.user_reg_button = QtWidgets.QPushButton(self.centralwidget)
        self.user_reg_button.setGeometry(QtCore.QRect(140, 230, 116, 28))
        self.user_reg_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.user_reg_button.setObjectName("user_reg_button")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.logo.setText("")
        self.logo.setStyleSheet("background-color: #000407;\n")
        self.logo.setPixmap(QtGui.QPixmap(r"C:\Users\Clayton\Desktop\Semister1\CT4029 - Principles of Programming\Assigment\Ass-2049\logo.png"))
        self.logo.setObjectName("logo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 306, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #registering functions to buttons
        self.user_login_button.clicked.connect(self.user_login)
        self.buiss_login_button.clicked.connect(self.busin_login)
        self.user_reg_button.clicked.connect(self.go_to_user_reg)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.user_login_button.setText(_translate("MainWindow", "User Login"))
        self.buiss_login_button.setText(_translate("MainWindow", "Business Login"))
        self.user_reg_button.setText(_translate("MainWindow", "User Register"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = landing_Page()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())