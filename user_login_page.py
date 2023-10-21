import sys
import random
import smtplib
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import md5
from main_page_demo import PromotionsApp


class user_login(QMainWindow):
    def go_to_main_page(self):
            self.close()
            self.ui.window = user_login()
            self.ui.window.show()            
    def user_login_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Congratulations! You have successfully logged in")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        self.go_to_main_page()
    def OTP_Sent_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("OTP has been sent to your email")
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
    def OTP_failure(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Your OTP is incorrect")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
    def gen_otp(self):
        otp = f'{random.randint(0, 9999):04d}'
        return otp
    def opt_send(self, otp_code):
        _translate = QtCore.QCoreApplication.translate
        sender_email = 'cgatting@gmail.com'
        recipient_email = self.email_address.text()
        print(recipient_email)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'cgatting@gmail.com'
        smtp_password = 'oytu gdvz jnkt uyjh'
        subject = 'Your OTP'
        message = f'Your OTP is: {otp_code}'
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        self.OTP_Sent_message()
        server.quit()
    def send_email(self):
        #Write username and password of self into an SQLite database
        _translate = QtCore.QCoreApplication.translate
        username = self.email_address.text()
        password = self.password.text()
        if username == '' or password == '':
            self.error_empty()
        else:
            password = md5(password.encode('utf-8')).hexdigest()
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            ##NEEDS CHANGING TO LOGIN INSTEAD
            c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = c.fetchone()
            if user is None:
                self.no_account()
            else:
                self.opt_send(OTP_USER_PASSWORD)
                pass
               
            conn.commit()
            conn.close()
    
    def opt_verify(self, otp_code):
        _translate = QtCore.QCoreApplication.translate
        if otp_code == self.opt.text():
            self.user_login_message()
        else:
            self.OTP_failure()

    def setupUi(self, MainWindow):
        global OTP_USER_PASSWORD
        OTP_USER_PASSWORD = self.gen_otp()
        print(OTP_USER_PASSWORD)
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
        self.main_box.setObjectName("main_box")
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
        self.send_email_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_email_button.setGeometry(QtCore.QRect(150, 310, 121, 28))
        self.send_email_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.send_email_button.setCheckable(False)
        self.send_email_button.setObjectName("send_email_button")
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
        self.logo.setPixmap(QtGui.QPixmap(r"C:\Users\Clayton\Desktop\Semister1\CT4029 - Principles of Programming\Assigment\Ass-2049\UI Files\logo.png"))
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
        self.send_email_button.clicked.connect(lambda: self.send_email())
        self.confirmation_button.clicked.connect(lambda: self.opt_verify(OTP_USER_PASSWORD))
        global user_email
        user_email = self.email_address.text()
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.opt.setPlaceholderText(_translate("MainWindow", "OTP"))
        self.send_email_button.setText(_translate("MainWindow", "Send Email"))
        self.confirmation_button.setText(_translate("MainWindow", "Confirm Registration"))
        self.forgot_password_button.setText(_translate("MainWindow", "Forgot Password"))
