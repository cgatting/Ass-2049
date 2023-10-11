from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import smtplib
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


class PromotionsApp(QMainWindow):
    def email_QR(self, QR_code, code, text):
        _translate = QtCore.QCoreApplication.translate
        sender_email = 'cgatting@gmail.com'  # Replace with your email
        recipient_email = 'cgatting@gmail.com'  # Replace with the recipient's email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'cgatting@gmail.com'
        smtp_password = 'oytu gdvz jnkt uyjh'  # Replace with your email password
        subject = 'Heres your QRlife email with your QR code'

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

    def filter_promotions(self, search_text, container_layout):
        # Clear existing promotions
        for i in reversed(range(container_layout.count())):
            container_layout.itemAt(i).widget().setParent(None)
            
        # Filter and display promotions matching the search_text
        filtered_promotions = [promotion for promotion in self.promotions if search_text.lower() in promotion[1].lower()]
        for promotion in filtered_promotions:
            promotion_widget = self.create_promotion_widget(promotion)
            container_layout.addWidget(promotion_widget)

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()

    def initUI(self):
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

        logo_label = QLabel()
        logo_label.setPixmap(
            QPixmap(
                r"C:\Users\cgatt\Desktop\Semester1\CT4029 - Principles of Programming\Assignment\Ass-2049\images\Logo.png"))
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

        self.create_promotions_table()
        self.promotions = self.fetch_promotions_from_database()

        for promotion in self.promotions:
            promotion_widget = self.create_promotion_widget(promotion)
            container_layout.addWidget(promotion_widget)

        self.update_date_time_labels(date_label, time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_date_time_labels(date_label, time_label))
        self.timer.start(1000)

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
        cursor.execute("SELECT text, voucher_code FROM promotions")
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

        text_label = QLabel(f"Text: {promotion[0]}")
        text_label.setFont(QFont("Arial", 20, QFont.Bold))
        text_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        voucher_label = QLabel(f"Voucher Code: {promotion[1]}")
        voucher_label.setFont(QFont("Arial", 16, QFont.Bold))
        voucher_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        email_button = QPushButton("Send to Email")
        email_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        save_button = QPushButton("Save Locally")
        save_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        email_button.clicked.connect(lambda _, qr_code=f"temp_qr_{promotion[1]}.png", code = promotion[1], text=promotion[0]: self.email_QR(qr_code, code, text))
        save_button.clicked.connect(lambda _, qr_code_pixmap=qr_pixmap, current_promotion=promotion: self.save_locally(qr_code_pixmap, current_promotion))
        promotion_layout.addWidget(text_label)
        promotion_layout.addWidget(voucher_label)
        promotion_layout.addWidget(qr_code_label)
        promotion_layout.addWidget(email_button)
        promotion_layout.addWidget(save_button)

        return promotion_widget

    def add_promotion_to_database(self, qr_code, text, voucher_code, dialog):
        conn = sqlite3.connect("promotions.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO promotions (qr_code, text, voucher_code) VALUES (?, ?, ?)", (qr_code, text, voucher_code))
        conn.commit()
        conn.close()

        self.promotions = self.fetch_promotions_from_database()
        self.update_ui_with_new_promotion()
        dialog.accept()

    def update_ui_with_new_promotion(self):
        for i in reversed(range(self.centralWidget().layout().count())):
            self.centralWidget().layout().itemAt(i).widget().setParent(None)

        container_widget = self.centralWidget().findChild(QWidget)
        container_layout = container_widget.layout()
        for promotion in self.promotions:
            count = 0
            promotion_widget = self.create_promotion_widget(promotion)
            container_layout.addWidget(promotion_widget)
            count += 1

    def update_date_time_labels(self, date_label, time_label):
        current_date = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
        current_time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)

        date_label.setText(f"Date: {current_date}")
        time_label.setText(f"Time: {current_time}")

    def logout(self):
        logging.basicConfig(
        filename="logging_file.txt",
        level=logging.INFO,
        format='%(asctime)s - USER LOGGED OUT'
    )

        logger = logging.getLogger()
        logger.info('')
        exit()

    def login(self):
        logging.basicConfig(
            filename="logging_file.txt",
            level=logging.INFO,
            format='%(asctime)s - USER LOGGED In'
        )

        logger = logging.getLogger()
        logger.info('')

        
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
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.email_address.setPalette(palette)
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
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.password.setPalette(palette)
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
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
    
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

    def main_page(self, first_name):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

    # Execute a query to retrieve the first_name
        query = "SELECT first_name FROM your_table_name WHERE your_condition_here;"
        cursor.execute(query)

        # Fetch the first_name (assuming there's only one result)
        result = cursor.fetchone()

        if result:
            first_name = result[0]
            print("First Name:", first_name)
        else:
            print("User not found or no data returned.")

        conn.close()
        MainWindow.close()
        first_namse = first_name
        ui = PromotionsApp(first_name=first_name)
        ui.setupUi(MainWindow)
        MainWindow.show()
        
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
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.email_address.setPalette(palette)
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
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.password.setPalette(palette)
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
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(175, 44, 116))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.opt.setPalette(palette)
        self.opt.setTabletTracking(False)
        self.opt.setAutoFillBackground(False)
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

class user_reg_page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("Registration Page")
        self.resize(300, 472)
        
        # Create a QVBoxLayout as the main layout for the page
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setObjectName("mainLayout")

        # Create a QFormLayout to organize the form elements (labels and input fields)
        self.formLayout = QtWidgets.QFormLayout()
        
        # Create and configure the input fields
        self.email_address = QtWidgets.QLineEdit()
        self.email_address.setPlaceholderText("Email Address")
        self.formLayout.addRow("Email Address:", self.email_address)
        
        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("Password")
        self.formLayout.addRow("Password:", self.password)
        
        self.opt = QtWidgets.QLineEdit()
        self.opt.setPlaceholderText("OTP")
        self.formLayout.addRow("OTP:", self.opt)

        # Create the "Send Email" button and configure its appearance
        self.send_email_button = QtWidgets.QPushButton("Send Email")
        self.send_email_button.setStyleSheet("QPushButton{background-color: #000407; color: white;}"
                                             "QPushButton::pressed {background-color: #edb518;}")
        self.formLayout.addRow(self.send_email_button)

        # Create the "Confirm Registration" button and configure its appearance
        self.confirmation_button = QtWidgets.QPushButton("Confirm Registration")
        self.confirmation_button.setStyleSheet("QPushButton{background-color: #000407; color: white;}"
                                               "QPushButton::pressed {background-color: #edb518;}")
        self.formLayout.addRow(self.confirmation_button)

        # Create and configure the logo label
        self.logo = QtWidgets.QLabel()
        self.logo.setStyleSheet("QLabel{background-color: #000407;}")
        self.logo.setPixmap(QtGui.QPixmap("C:\\Users\\cgatt\\Desktop\\Semister1\\CT4029 - Principles of Programming\\Assigment\\Ass-2049\\UI Files\\../images/Logo.png"))
        self.formLayout.addRow(self.logo)

        # Connect button clicks to methods
        self.send_email_button.clicked.connect(self.opt_send)
        self.confirmation_button.clicked.connect(self.opt_verify)
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
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.opt.setPlaceholderText(_translate("MainWindow", "OTP"))
        self.send_email_button.setText(_translate("MainWindow", "Send Email"))
        self.confirmation_button.setText(_translate("MainWindow", "Confirm Registration"))
class LandingPage(object):
    def user_reg(self):
        self.close_and_open(user_reg_page)

    def user_login(self):
        self.close_and_open(user_login_page)

    def busin_login(self):
        self.close_and_open(business_login_page)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Landing_Page")
        MainWindow.resize(306, 479)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_page = QtWidgets.QLabel(self.centralwidget)
        self.main_page.setGeometry(QtCore.QRect(0, 0, 290, 410))
        self.main_page.setStyleSheet("background-color: #79031D;\nborder-radius: 10px")
        self.main_page.setText("")
        self.main_page.setObjectName("main_page")
        
        # Define buttons
        self.user_login_button = self.create_button("User Login", 20, 230, self.user_login)
        self.buiss_login_button = self.create_button("Business Login", 20, 270, self.busin_login)
        self.user_reg_button = self.create_button("User Register", 140, 230, self.user_reg)
        
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.logo.setStyleSheet("background-color: #000407;")
        self.logo.setPixmap(QtGui.QPixmap("C:\\Users\\cgatt\\Desktop\\Semister1\\CT4029 - Principles of Programming\\Assigment\\Ass-2049\\UI Files\\../images/Logo.png"))
        self.logo.setObjectName("logo")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_button(self, text, x, y, callback):
        button = QtWidgets.QPushButton(self.centralwidget)
        button.setGeometry(QtCore.QRect(x, y, 116, 28))
        button.setText(text)
        button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        button.clicked.connect(callback)
        return button

    def close_and_open(self, page):
        MainWindow.close()
        ui = page()
        ui.initUI()
        MainWindow.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Landing Page"))
        # Define button text translations here

if __name__ == "__main__":
    otp_code = "1111"
    # otp_code = user_reg_page.gen_otp()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = LandingPage()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())