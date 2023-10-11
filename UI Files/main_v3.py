from PyQt5 import QtWidgets, QtCore, QtGui, QtCore
import smtplib
from PyQt5.QtWidgets import QMessageBox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import sys
import sqlite3

"""
color palette
#F5F7F7
#edb518
#79031D
#000407
"""
##NEED TO LINK AFTER LOGIN TO MAIN APPLICATION PAGE
class business_login_page(object):        
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
        msg.setText("You do not have an account")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
    def user_login(self):
        #Write username and password of self into an SQLite database
        _translate = QtCore.QCoreApplication.translate
        username = self.email_address.text()
        password = self.password.text()
        if username == '' or password == '':
            self.error_empty()
        else:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            ##NEEDS CHANGING TO LOGIN INSTEAD
            c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = c.fetchone()
            if user is None:
                self.no_account()
            else:
                ##NOW NEED TO LOGIN TO MAIN APPLICATION PAGE
                pass
                
            # conn.commit()
            # conn.close()

    def setupUi(self, MainWindow):
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

    
        self.send_email_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_email_button.setGeometry(QtCore.QRect(150, 310, 121, 28))
        self.send_email_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.send_email_button.setCheckable(False)
        self.send_email_button.setObjectName("send_email_button")
        self.confirmation_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirmation_button.setGeometry(QtCore.QRect(20, 360, 261, 28))
        self.confirmation_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")

        self.confirmation_button.setCheckable(False)
        self.confirmation_button.setObjectName("confirmation_button")
        
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.logo.setText("")
        self.logo.setStyleSheet("QLabel{background-color: #000407;}")
        self.logo.setPixmap(QtGui.QPixmap("C:\\Users\\cgatt\\Desktop\\Semister1\\CT4029 - Principles of Programming\\Assigment\\Ass-2049\\UI Files\\../images/Logo.png"))
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
        # self.confirmation_button.clicked.connect(lambda: self.opt_verify(otp_code=otp_code))



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.send_email_button.setText(_translate("MainWindow", "Send Email"))
        self.confirmation_button.setText(_translate("MainWindow", "Confirm Registration"))

class user_login_page(object):
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
        msg.setText("You do not have an account")
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
    def user_login(self):
        #Write username and password of self into an SQLite database
        _translate = QtCore.QCoreApplication.translate
        username = self.email_address.text()
        password = self.password.text()
        if username == '' or password == '':
            self.error_empty()
        else:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            ##NEEDS CHANGING TO LOGIN INSTEAD
            c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = c.fetchone()
            if user is None:
                self.no_account()
            else:
                ##NOW NEED TO LOGIN TO MAIN APPLICATION PAGE
                pass
               
            # conn.commit()
            # conn.close()
    
    def opt_verify(self, otp_code):
        _translate = QtCore.QCoreApplication.translate
        if otp_code == self.opt.text():
            self.user_login()
        else:
            self.send_email_button.setText(_translate("MainWindow",  "Invalid OTP"))
        self.user_login()


    def setupUi(self, MainWindow):
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
        self.confirmation_button.setGeometry(QtCore.QRect(20, 360, 261, 28))
        self.confirmation_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")

        self.confirmation_button.setCheckable(False)
        self.confirmation_button.setObjectName("confirmation_button")
        
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.logo.setText("")
        self.logo.setStyleSheet("QLabel{background-color: #000407;}")
        self.logo.setPixmap(QtGui.QPixmap("C:\\Users\\cgatt\\Desktop\\Semister1\\CT4029 - Principles of Programming\\Assigment\\Ass-2049\\UI Files\\../images/Logo.png"))
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
        self.send_email_button.clicked.connect(lambda: self.opt_send(otp_code=otp_code))
        self.confirmation_button.clicked.connect(lambda: self.opt_verify(otp_code=otp_code))



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.opt.setPlaceholderText(_translate("MainWindow", "OTP"))
        self.send_email_button.setText(_translate("MainWindow", "Send Email"))
        self.confirmation_button.setText(_translate("MainWindow", "Confirm Registration"))


class user_reg_page(object):
    def error_empty(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You need to enter a username or password")
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
        self.send_email_button.setText(_translate("MainWindow",  "OTP Sent!"))
    def user_register(self):
        username = self.email_address.text()
        password = self.password.text()
        
        if username == '' or password == '':
            self.error_empty()
        else:
            try:
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                
                # Create the 'users' table if it doesn't exist
                c.execute('''CREATE TABLE IF NOT EXISTS users(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT,
                            password TEXT)''')
                
                # Insert the user's information into the 'users' table
                c.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
                
                # Commit changes and close the connection
                conn.commit()
                conn.close()
            except sqlite3.Error as e:
                # Handle any potential database errors here
                print("SQLite error:", e)
        
    def opt_verify(self, otp_code):
        if otp_code == self.opt.text():
            self.user_register()
        else:
            self.OTP_failure()
        self.user_register()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Registration Page")
        MainWindow.resize(300, 472)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 450, 600))
        self.widget.setObjectName("widget")
        self.main_box = QtWidgets.QLabel(self.centralwidget)
        self.main_box.setGeometry(QtCore.QRect(0, 0, 290, 410))
        self.main_box.setStyleSheet("background-color:#79031D;")
        self.main_box.setText("")
        self.main_box.setObjectName("main_box")
        self.email_address = QtWidgets.QLineEdit(self.centralwidget)
        self.email_address.setGeometry(QtCore.QRect(20, 210, 250, 30))
        self.email_address.setTabletTracking(False)
        self.email_address.setAutoFillBackground(False)
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
        self.password.setTabletTracking(False)
        self.password.setAutoFillBackground(False)
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
        self.confirmation_button.setGeometry(QtCore.QRect(20, 360, 261, 28))
        self.confirmation_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.confirmation_button.setCheckable(False)
        self.confirmation_button.setObjectName("confirmation_button")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.logo.setText("")
        self.logo.setStyleSheet("QLabel{background-color: #000407;}")
        self.logo.setPixmap(QtGui.QPixmap("C:\\Users\\cgatt\\Desktop\\Semister1\\CT4029 - Principles of Programming\\Assigment\\Ass-2049\\UI Files\\../images/Logo.png"))
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
        self.send_email_button.clicked.connect(lambda: self.opt_send(otp_code=otp_code))
        self.confirmation_button.clicked.connect(lambda: self.opt_verify(otp_code=otp_code))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.opt.setPlaceholderText(_translate("MainWindow", "OTP"))
        self.send_email_button.setText(_translate("MainWindow", "Send Email"))
        self.confirmation_button.setText(_translate("MainWindow", "Confirm Registration"))

class landing_Page(object):
    def user_reg(self):
        MainWindow.close()
        ui = user_reg_page()
        ui.setupUi(MainWindow)
        MainWindow.show()
    def user_login(self):
        MainWindow.close()
        ui = user_login_page()
        ui.setupUi(MainWindow)
        MainWindow.show()
    def busin_login(self):
        MainWindow.close()
        ui = business_login_page()
        ui.setupUi(MainWindow)
        MainWindow.show()

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
        self.terms_button = QtWidgets.QPushButton(self.centralwidget)
        self.terms_button.setGeometry(QtCore.QRect(20, 310, 116, 28))
        self.terms_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.terms_button.setObjectName("terms_button")
        self.conact_button = QtWidgets.QPushButton(self.centralwidget)
        self.conact_button.setGeometry(QtCore.QRect(140, 310, 116, 28))
        self.conact_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.conact_button.setObjectName("conact_button")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.logo.setText("")
        self.logo.setStyleSheet("background-color: #000407;\n")
        self.logo.setPixmap(QtGui.QPixmap("C:\\Users\\cgatt\\Desktop\\Semister1\\CT4029 - Principles of Programming\\Assigment\\Ass-2049\\UI Files\\../images/Logo.png"))
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
        self.user_reg_button.clicked.connect(self.user_reg)
        # self.terms_button.clicked.connect(self.terms)
        # self.conact_button.clicked.connect(self.contact)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.user_login_button.setText(_translate("MainWindow", "User Login"))
        self.buiss_login_button.setText(_translate("MainWindow", "Business Login"))
        self.user_reg_button.setText(_translate("MainWindow", "User Register"))
        self.terms_button.setText(_translate("MainWindow", "Terms Contracts"))
        self.conact_button.setText(_translate("MainWindow", "Contact Us"))

if __name__ == "__main__":
    otp_code = "1111"
    # otp_code = user_reg_page.gen_otp()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = landing_Page()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())