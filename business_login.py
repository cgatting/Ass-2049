import sys
import random
import smtplib
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import md5
from business_main import BusinessMainPage
#!NEED TO GO THROUGH AND REMOVE OTP AND REMOVE SMTP
#!NEED TO GO THROUGH AND ADD SQL
#!NEED TO GO THORUGH AND ADD LOGIC TO NEXT PAGE
#!NEED TO ADD LOGIC TO FOGOTTEN EMAIL MAYBE A POP UP BOX AND EDIT FUNCTION

class Business_Login_Page(QMainWindow):
    def go_to_main_page(self, user_email):
        self.hide()  # Hide the current window (login page)
        self.ui = BusinessMainPage(user_email)  # Create an instance of the BusinessMainPage
        self.ui.show()        
    def user_login_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Congratulations! You have successfully logged in")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
    def error_empty(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You need to enter a username or password")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
    def no_account(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Either details are incorrect or you do not have an account yet")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
    def check_account(self):
        _translate = QtCore.QCoreApplication.translate
        username = self.email_address.text()
        password = self.password.text()
        if username == '' or password == '':
            self.error_empty()
        else:
            password = md5(password.encode('utf-8')).hexdigest()
            conn = sqlite3.connect('business.db')
            c = conn.cursor()
            ##NEEDS CHANGING TO LOGIN INSTEAD
            c.execute('SELECT * FROM accounts WHERE email = ? AND password = ?', (username, password))
            user = c.fetchone()
            if user is None:
                self.no_account()
            else:
                self.go_to_main_page(username)
                pass

    def __init__(self, MainWindow):
        super().__init__()
        MainWindow.setObjectName("Login Page")
        MainWindow.resize(300, 472)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 450, 600))
        self.widget.setObjectName("widget")
        self.main_box = QtWidgets.QLabel(self.centralwidget)
        self.main_box.setGeometry(QtCore.QRect(0, 0, 290, 410))
        self.main_box.setStyleSheet("background-color:#79031D;\n"
"border-radius: 10px")
        self.main_box.setText("")
        self.main_box.setObjectName("")
        self.email_address = QtWidgets.QLineEdit(self.centralwidget)
        self.email_address.setGeometry(QtCore.QRect(20, 210, 250, 30))
        self.email_address.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border: 1px solid rgba(0, 0, 0, 0);\n"
"border-bottom-color: rgba(0, 0, 0, 255);\n"
"padding-bottom: 7px;\n"
"color: #F5F7F7;")
        self.email_address.setText("")
        self.email_address.setCursorPosition(0)
        self.email_address.setObjectName("email_address")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(20, 260, 250, 30))
        self.password.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border: 1px solid rgba(0, 0, 0, 0);\n"
"border-bottom-color: rgba(0, 0, 0, 255);\n"
"padding-bottom: 7px;\n"
"color: #F5F7F7;")
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.opt = QtWidgets.QLineEdit(self.centralwidget)
        self.opt.setGeometry(QtCore.QRect(20, 310, 121, 30))
        self.opt.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border: 1px solid rgba(0, 0, 0, 0);\n"
"border-bottom-color: rgba(0, 0, 0, 255);\n"
"padding-bottom: 7px;\n"
"color: #F5F7F7;")
        self.opt.setInputMask("")
        self.opt.setText("")
        self.opt.setMaxLength(4)
        self.opt.setClearButtonEnabled(False)
        self.opt.setObjectName("opt")
        
        self.confirmation_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirmation_button.setGeometry(QtCore.QRect(20, 350, 261, 28))
        self.confirmation_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.confirmation_button.setCheckable(False)
        self.confirmation_button.setObjectName("confirmation_button")
        self.forgot_password_button = QtWidgets.QPushButton(self.centralwidget)
        self.forgot_password_button.setGeometry(QtCore.QRect(20, 380, 261, 28))
        self.forgot_password_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.forgot_password_button.setCheckable(False)
        self.forgot_password_button.setObjectName("forgot_password_button")
        
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.logo.setText("")
        self.logo.setStyleSheet("QLabel{background-color: #000407;}")
        self.logo.setPixmap(QtGui.QPixmap(r"C:\Users\Clayton\Desktop\Semister1\CT4029 - Principles of Programming\Assigment\Ass-2049\logo.png"))
        self.logo.setObjectName("logo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.confirmation_button.clicked.connect(lambda: self.check_account())
        global user_email
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "This is the Login Page"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.opt.setPlaceholderText(_translate("MainWindow", "Business Code"))
        self.confirmation_button.setText(_translate("MainWindow", "Confirm Registration"))
        self.forgot_password_button.setText(_translate("MainWindow", "Forgot Password"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Business_Login_Page(MainWindow)
    MainWindow.show() 
    sys.exit(app.exec_())