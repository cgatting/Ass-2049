from PyQt5 import QtWidgets, QtGui, QtCore
import smtplib
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QScrollArea, QDialog, QLineEdit, QVBoxLayout as QVBox, QHBoxLayout, QFrame, QFileDialog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from hashlib import md5
import sys
import sqlite3
import qrcode
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QDate, QTime, QDir
import logging
from email.mime.image import MIMEImage
import os
import datetime

"""
color palette
#F5F7F7
#edb518
#79031D
#000407
"""
class PromotionsApp(QMainWindow):  
    
    def email_QR(self, QR_code, code, text):
        sender_email = 'cgatting@gmail.com'  # Replace with your email
        recipient_email = 'cgatting@gmail.com'  # Replace with the recipient's email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'cgatting@gmail.com'
        smtp_password = 'oytu gdvz jnkt uyjh'  # Replace with your email password
        subject = "Here's your QRlife email with your QR code"

        # Create a message with the QR code as an attachment and include the voucher code and text description in the email body
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach the QR code image to the email
        with open(QR_code, 'rb') as qr_file:
            qr_attachment = MIMEImage(qr_file.read())
        message.attach(qr_attachment)

        # Add the voucher code and text description to the email body
        email_body = f"Here is your QR code for the promotion:\n\nVoucher Code: {code}\nText Description: {text}"
        text_part = MIMEText(email_body, 'plain')
        message.attach(text_part)

        # Connect to the SMTP server and send the email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            server.quit()
            logging.info('Email sent successfully')
        except Exception as e:
            logging.error('Error sending email: %s', str(e))

    def save_locally(self, qr_code_pixmap, promotion):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Allow only selecting directories

        directory = QFileDialog.getExistingDirectory(self, "Select a directory to save the QR code", QDir.homePath(), options=options)

        if directory:
            # Now you have the selected directory in 'directory'
            # You can save the QR code in this directory
            save_path = os.path.join(directory, f"temp_qr_{promotion}.png")
            qr_code_pixmap.save(save_path)

    def update_remaining_time_label(self, remaining_time_label, end_time):
        remaining_time = end_time - datetime.datetime.now()
        remaining_time -= datetime.timedelta(microseconds=remaining_time.microseconds)
        remaining_time_label.setText(f"Time Remaining: {remaining_time}")

    def filter_promotions(self, search_text, container_layout):
        # Clear existing promotions
        for i in reversed(range(container_layout.count())):
            container_layout.itemAt(i).widget().setParent(None)

        # Filter and display promotions matching the search_text
        filtered_promotions = [promotion for promotion in self.promotions if search_text.lower() in promotion[1].lower()]
        for promotion in filtered_promotions:
            promotion_widget = self.create_promotion_widget(promotion)
            container_layout.addWidget(promotion_widget)

    def setupUi(self, MainWindow):
        self.setWindowTitle("Promotions Dashboard")
        self.setGeometry(0, 0, 1020, 600)
        self.setWindowIcon(QIcon("icon.png"))

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f5f5f5;")
        self.setCentralWidget(central_widget)
        central_widget_layout = QVBoxLayout()
        central_widget.setLayout(central_widget_layout)
        search_label = QLabel("Search:")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Enter search criteria...")
        search_input.textChanged.connect(lambda: self.filter_promotions(search_input.text(), container_layout))
        central_widget_layout.addWidget(search_label)
        central_widget_layout.addWidget(search_input)

        header_widget = QFrame()
        header_widget.setStyleSheet("background-color: #000407; border-bottom: 1px solid #000407;")
        header_layout = QHBoxLayout()
        header_widget.setLayout(header_layout)

        # Add the Welcome User label
        welcome_label = QLabel("")
        welcome_label.setStyleSheet("QLabel { color: white; font-size: 20px; }")
        
        header_layout.addWidget(welcome_label)

        # Add your logo here (replace path)
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(r"path_to_logo.png"))
        header_layout.addWidget(logo_label)
        date_label = QLabel()
        date_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        time_label = QLabel()
        time_label.setStyleSheet("QLabel { color : #F5F7F7; }")

        header_layout.addStretch(1)
        header_layout.addWidget(date_label)
        header_layout.addWidget(time_label)

        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet("QPushButton{background-color: #edb518; color: white;} QPushButton::pressed {background-color: #f3cc5f;}")
        logout_button.clicked.connect(self.logout)
        header_layout.addWidget(logout_button)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        central_widget_layout.addWidget(header_widget)
        central_widget_layout.addWidget(scroll_area)

        container_widget = QWidget()
        scroll_area.setWidget(container_widget)
        container_layout = QVBoxLayout()
        container_widget.setLayout(container_layout)
        container_widget.setStyleSheet("border-radius: 10px;")
        scroll_area.setStyleSheet("border-radius: 10px;")

        self.create_promotions_table()
        self.promotions = self.fetch_promotions_from_database()

        for promotion in self.promotions:
            promotion_widget = self.create_promotion_widget(promotion)
            container_layout.addWidget(promotion_widget)

        self.show()

    def create_promotions_table(self):
        conn = sqlite3.connect("promotions.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                voucher_code TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def fetch_promotions_from_database(self):
        conn = sqlite3.connect("promotions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM promotions")
        promotions = cursor.fetchall()
        conn.close()
        return promotions

    def create_promotion_widget(self, promotion):
        promotion_widget = QFrame()
        promotion_widget.setStyleSheet("background-color: #79031D;")
        promotion_layout = QVBoxLayout()
        promotion_widget.setLayout(promotion_layout)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
        qr.add_data(promotion[1])
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(f"temp_qr_{promotion[1]}.png")
        qr_pixmap = QPixmap(f"temp_qr_{promotion[1]}.png")
        qr_code_label = QLabel()
        qr_code_label.setPixmap(qr_pixmap)
        qr_code_label.setAlignment(Qt.AlignCenter)
        company_label = QLabel(f"Company: {promotion[-1]}")
        company_label.setFont(QFont("Arial", 24, QFont.Bold))
        company_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        text_label = QLabel(f"Text: {promotion[2]}")
        text_label.setFont(QFont("Arial", 20, QFont.Bold))
        text_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        voucher_label = QLabel(f"Voucher Code: {promotion[1]}")
        voucher_label.setFont(QFont("Arial", 16, QFont.Bold))
        voucher_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        email_button = QPushButton("Send to Email")
        email_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        save_button = QPushButton("Save Locally")
        email_button.setFont(QFont("Arial", 12, QFont.Bold))
        save_button.setFont(QFont("Arial", 12, QFont.Bold))
        save_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        start_time_label = QLabel(f"Start Time: {promotion[-2]}")
        end_time_label = QLabel(f"End Time: {promotion[-3]}")
        remaining_time_label = QLabel(f"Time Remaining: {datetime.datetime.strptime(promotion[-3], '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()}")
        end_time_label.move(20, 20)
        start_time_label.setFont(QFont("Arial", 10, QFont.Bold))
        end_time_label.setFont(QFont("Arial", 10, QFont.Bold))
        remaining_time_label.setFont(QFont("Arial", 10, QFont.Bold))
        start_time_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        end_time_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        remaining_time_label.setStyleSheet("QLabel { color : #F5F7F7; }")

        end_time = datetime.datetime.strptime(promotion[-3], '%Y-%m-%d %H:%M:%S')
        # Update the remaining time label periodically
        self.remaining_time_timer = QTimer(self)
        self.remaining_time_timer.timeout.connect(lambda: self.update_remaining_time_label(remaining_time_label, end_time))
        self.remaining_time_timer.start(100)

        ## ASSIGN THE BUTTON CLICK FUNCTIONS ##
        email_button.clicked.connect(lambda _, qr_code=f"temp_qr_{promotion[1]}.png", code=promotion[1], text=promotion[0]: self.email_QR(qr_code, code, text))
        save_button.clicked.connect(lambda _, qr_code_pixmap=qr_pixmap, current_promotion=promotion: self.save_locally(qr_code_pixmap, current_promotion))
        promotion_layout.addWidget(company_label)
        promotion_layout.addWidget(text_label)
        promotion_layout.addWidget(voucher_label)
        promotion_layout.addWidget(qr_code_label)
        promotion_layout.addWidget(start_time_label)
        promotion_layout.addWidget(end_time_label)
        promotion_layout.addWidget(remaining_time_label)
        promotion_layout.addWidget(email_button)
        promotion_layout.addWidget(save_button)

        return promotion_widget

    def logout(self):
        logging.basicConfig(
        filename="logging_file.txt",
        level=logging.INFO,
        format='%(asctime)s - USER LOGGED OUT'
    )

        logger = logging.getLogger()
        logger.info('')
        exit()
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
        # self.confirmation_button.clicked.connect(lambda: self.opt_verify(otp_code=otp_code))



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.send_email_button.setText(_translate("MainWindow", "Send Email"))
        self.confirmation_button.setText(_translate("MainWindow", "Confirm Registration"))

class user_login_page(object):
    def go_to_main_page(self):
        MainWindow.close()
        ui = PromotionsApp()
        ui.setupUi(MainWindow)
        MainWindow.show()
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

class user_reg_page(object):
    def user_login(self):
        self.user_register()
        self.login_successful()
        MainWindow.close()
        ui = user_login_page()
        ui.setupUi(MainWindow)
        MainWindow.show()
    def login_successful(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Login Successful")
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
    def failure(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Your information is incorrect")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

    def user_register(self):
        username = self.email_address.text()
        password = self.password.text()
        md5_hash_password = md5(password.encode()).hexdigest()
        first_name = self.first_name.text()
        last_name = self.last_name.text()
        DoB = self.dateEdit.text()
        if username == '' or password == '' or first_name == '' or last_name == '' or DoB == '':
            self.error_empty()
        else:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            
            # Create the 'users' table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    date_of_birth TEXT
                )''')
            
            # Insert the user's information into the 'users' table
            c.execute("INSERT INTO users (username, password, first_name, last_name, date_of_birth) VALUES(?,?,?,?,?)", (username, md5_hash_password, first_name, last_name, DoB))
            
            # Commit changes and close the connection
            conn.commit()
            conn.close()
           
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 472)
        MainWindow.setAcceptDrops(False)
        MainWindow.setAutoFillBackground(False)
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
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 270, 151))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(r"C:\Users\Clayton\Desktop\Semister1\CT4029 - Principles of Programming\Assigment\Ass-2049\UI Files\logo.png"))
        self.logo.setObjectName("logo")
        self.logo.setStyleSheet("background-color: #000407")
        self.email_address = QtWidgets.QLineEdit(self.centralwidget)
        self.email_address.setGeometry(QtCore.QRect(11, 171, 241, 27))
        self.email_address.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                        "border: 1px solid rgba(0, 0, 0, 0);\n"
                                        "border-bottom-color: rgba(0, 0, 0, 255);\n"
                                        "padding-bottom: 7px;\n"
                                        "color: #F5F7F7;")
        self.email_address.setText("")
        self.email_address.setCursorPosition(0)
        self.email_address.setObjectName("email_address")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(11, 205, 241, 27))
        self.password.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "border: 1px solid rgba(0, 0, 0, 0);\n"
                                   "border-bottom-color: rgba(0, 0, 0, 255);\n"
                                   "padding-bottom: 7px;\n"
                                   "color: #F5F7F7")
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.first_name = QtWidgets.QLineEdit(self.centralwidget)
        self.first_name.setGeometry(QtCore.QRect(11, 239, 108, 27))
        self.first_name.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                              "border: 1px solid rgba(0, 0, 0, 0);\n"
                              "border-bottom-color: rgba(0, 0, 0, 255);\n"
                              "padding-bottom: 7px;\n"
                              "color: #F5F7F7")
        self.first_name.setInputMask("")
        self.first_name.setText("")
        self.first_name.setMaxLength(255)
        self.first_name.setClearButtonEnabled(False)
        self.first_name.setObjectName("opt")
        self.last_name = QtWidgets.QLineEdit(self.centralwidget)
        self.last_name.setGeometry(QtCore.QRect(126, 239, 126, 27))
        self.last_name.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                "border: 1px solid rgba(0, 0, 0, 0);\n"
                                "border-bottom-color: rgba(0, 0, 0, 255);\n"
                                "padding-bottom: 7px;\n"
                                "color: #F5F7F7")
        self.last_name.setInputMask("")
        self.last_name.setText("")
        self.last_name.setMaxLength(255)
        self.last_name.setClearButtonEnabled(False)
        self.last_name.setObjectName("opt_2")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(11, 290, 108, 27))
        self.dateEdit.setObjectName("dateEdit")
        self.confirmation_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirmation_button.setGeometry(QtCore.QRect(126, 290, 126, 27))
        self.confirmation_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        self.confirmation_button.setCheckable(False)
        self.confirmation_button.setObjectName("confirmation_button")
        self.confirmation_button.setText("Confirm Registration")
        self.confirmation_button.clicked.connect(lambda: self.user_login())
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.first_name.setPlaceholderText(_translate("MainWindow", "First Name"))
        self.last_name.setPlaceholderText(_translate("MainWindow", "Last Name"))
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
        self.logo.setPixmap(QtGui.QPixmap(r"C:\Users\Clayton\Desktop\Semister1\CT4029 - Principles of Programming\Assigment\Ass-2049\UI Files\logo.png"))
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
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = landing_Page()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())