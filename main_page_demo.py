import sys
import sqlite3
import qrcode
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
    QScrollArea, QDialog, QLineEdit, QVBoxLayout as QVBox, QHBoxLayout, QFrame, QFileDialog
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QDate, QTime, QDir
from PyQt5 import QtCore
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

"""
color palette
#F5F7F7 - Text
#edb518 - Standout Buttons
#79031D - Background
#000407 - Seperate Boxes
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

    def __init__(self):
        super().__init__()
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
        container_widget.setStyleSheet("border-radius: 10px;")
        scroll_area.setStyleSheet("border-radius: 10px;")

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
        save_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        email_button.clicked.connect(lambda _, qr_code=f"temp_qr_{promotion[1]}.png", code = promotion[1], text=promotion[0]: self.email_QR(qr_code, code, text))
        save_button.clicked.connect(lambda _, qr_code_pixmap=qr_pixmap, current_promotion=promotion: self.save_locally(qr_code_pixmap, current_promotion))
        promotion_layout.addWidget(company_label)
        promotion_layout.addWidget(text_label)
        promotion_layout.addWidget(voucher_label)
        promotion_layout.addWidget(qr_code_label)
        promotion_layout.addWidget(email_button)
        promotion_layout.addWidget(save_button)

        return promotion_widget
    ##NEEDS EDITING
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

        

def main():
    app = QApplication(sys.argv)
    ex = PromotionsApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
