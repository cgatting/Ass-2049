import sqlite3  # Import the SQLite database module for data storage
import qrcode  # Import the qrcode library for generating QR codes
from PyQt5.QtWidgets import (  # Import GUI widgets from PyQt5 library
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton,
    QScrollArea, QFrame, QFileDialog, QLineEdit, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont, QIcon  # Import classes for GUI styling
from PyQt5.QtCore import Qt, QTimer  # Import classes for GUI core functionality
import logging  # Import the logging module for creating log files
import smtplib  # Import the smtplib library for sending emails
from email.mime.text import MIMEText  # Import classes for creating email content
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os, sys  # Import the os module for working with the operating system
import datetime  # Import the datetime module for handling date and time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDesktopWidget  # Import QDesktopWidget


# Define a color palette using hexadecimal color codes
"""
color palette
#F5F7F7 - Text
#edb518 - Standout Buttons
#79031D - Background
#000407 - Separate Boxes
"""

class PromotionsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.promotion_timers = {}
        # Set up the main user interface
        MainWindow.setWindowTitle("Promotions Dashboard")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())        # MainWindow.setGeometry(0, 0, 1020, 600)
        MainWindow.setWindowIcon(QIcon("icon.png"))

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f5f5f5;")
        self.setCentralWidget(central_widget)
        central_widget_layout = QVBoxLayout()
        central_widget.setLayout(central_widget_layout)

        search_label = QLabel("Search:")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Enter search criteria...")

        # Connect the search input to the filter_promotions method when text is changed
        search_input.textChanged.connect(lambda: self.filter_promotions(search_input.text(), container_layout))

        central_widget_layout.addWidget(search_label)
        central_widget_layout.addWidget(search_input)

        header_widget = QFrame()
        header_widget.setStyleSheet("background-color: #000407; border-bottom: 1px solid #000407;")
        header_layout = QHBoxLayout()
        header_widget.setLayout(header_layout)

        # Create a QLabel for the "Welcome User" message
        welcome_label = QLabel("")

        # Apply styling to the welcome label
        welcome_label.setStyleSheet("QLabel { color: white; font-size: 20px; }")

        # Create a QLabel for the logo (replace path_to_logo.png)
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(r"path_to_logo.png"))

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

        header_layout.addWidget(welcome_label)
        header_layout.addWidget(logo_label)
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

        # Create the promotions table in the database if it doesn't exist
        self.create_promotions_table()

        # Fetch promotions from the database
        self.promotions = self.fetch_promotions_from_database()

        # Create promotion widgets and add them to the layout
        for promotion in self.promotions:
            promotion_widget = self.create_promotion_widget(promotion)
            container_layout.addWidget(promotion_widget)

        self.show()

    def email_QR(self, QR_code, code, text):
        # Email sending configuration
        sender_email = 'cgatting@gmail.com'
        recipient_email = 'cgatting@gmail.com'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'cgatting@gmail.com'
        smtp_password = 'oytu gdvz jnkt uyjh'
        subject = "Here's your QRlife email with your QR code"

        # Create an email message with the QR code attachment
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

        # Open a file dialog for selecting a directory to save the QR code
        directory = QFileDialog.getExistingDirectory(self, "Select a directory to save the QR code", QDir.homePath(), options=options)

        if directory:
            # Save the QR code in the selected directory
            save_path = os.path.join(directory, f"temp_qr_{promotion}.png")
            qr_code_pixmap.save(save_path)

    def update_remaining_time_label(self, remaining_time_label, end_time):
        if remaining_time_label:
            # Calculate the remaining time and update the label
            remaining_time = end_time - datetime.datetime.now()
            remaining_time -= datetime.timedelta(microseconds=remaining_time.microseconds)
            remaining_time_label.setText(f"Time Remaining: {remaining_time}")

    def filter_promotions(self, search_text, container_layout):
        # Stop and clean up existing timers
        for promotion in self.promotions:
            if hasattr(promotion, 'timer'):
                promotion.timer.stop()
                promotion.timer.deleteLater()

        # Clear existing promotions from the layout
        for i in reversed(range(container_layout.count())):
            widget = container_layout.itemAt(i).widget()
            container_layout.removeWidget(widget)

        # Filter and display promotions matching the search text
        filtered_promotions = [promotion for promotion in self.promotions if search_text.lower() in promotion[1].lower()]
        for promotion in filtered_promotions:
            promotion_widget = self.create_promotion_widget(promotion)
            container_layout.addWidget(promotion_widget)

        

    def create_promotions_table(self):
        conn = sqlite3.connect("promotions.db")
        cursor = conn.cursor()

        # Create the "promotions" table in the database if it doesn't exist
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

        # Retrieve all promotions from the "promotions" table
        cursor.execute("SELECT * FROM promotions")
        promotions = cursor.fetchall()
        conn.close()
        return promotions

    def create_promotion_widget(self, promotion):
        promotion_widget = QFrame()
        promotion_widget.setStyleSheet("background-color: #79031D;")
        promotion_layout = QVBoxLayout()
        promotion_widget.setLayout(promotion_layout)

        remaining_time_label = QLabel()
        remaining_time_label.setFont(QFont("Arial", 10, QFont.Bold))
        remaining_time_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        end_time = datetime.datetime.strptime(promotion[-3], '%d/%m/%Y %H:%M')

        # Calculate and display the initial time remaining
        remaining_time = end_time - datetime.datetime.now()
        remaining_time -= datetime.timedelta(microseconds=remaining_time.microseconds)
        remaining_time_label.setText(f"Time Remaining: {remaining_time}")

        company_label = QLabel(f"Company: {promotion[-1]}")
        company_label.setFont(QFont("Arial", 24, QFont.Bold))
        company_label.setStyleSheet("QLabel { color : #F5F7F7; }")

        text_label = QLabel(f"Text: {promotion[2]}")
        text_label.setFont(QFont("Arial", 20, QFont.Bold))
        text_label.setStyleSheet("QLabel { color : #F5F7F7; }")

        voucher_label = QLabel(f"Voucher Code: {promotion[1]}")
        voucher_label.setFont(QFont("Arial", 16, QFont.Bold))
        voucher_label.setStyleSheet("QLabel { color : #F5F7F7; }")

        # Generate a QR code for the voucher code
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
        qr_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Use AlignmentFlag to set alignment

        email_button = QPushButton("Send to Email")
        email_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        email_button.setFont(QFont("Arial", 12, QFont.Bold))

        save_button = QPushButton("Save Locally")
        save_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        save_button.setFont(QFont("Arial", 12, QFont.Bold))

        start_time_label = QLabel(f"Start Time: {promotion[-3]}")
        end_time_label = QLabel(f"End Time: {promotion[-2]}")
        remaining_time_label.setFont(QFont("Arial", 10, QFont.Bold))
        start_time_label.setStyleSheet("QLabel { color : #F5F7F7; }")
        end_time_label.setStyleSheet("QLabel { color : #F5F7F7; }")

        end_time = datetime.datetime.strptime(promotion[-2], '%d/%m/%Y %H:%M')

        # Update the remaining time label periodically using a timer
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.update_remaining_time_label(remaining_time_label, end_time))
        timer.start(100)

        # Connect email and save button actions to their respective functions
        email_button.clicked.connect(lambda _, qr_code=f"temp_qr_{promotion[1]}.png", code=promotion[1], text=promotion[0]: self.email_QR(qr_code, code, text))
        save_button.clicked.connect(lambda _, qr_code_pixmap=qr_pixmap, current_promotion=promotion: self.save_locally(qr_code_pixmap, current_promotion))

        # Add widgets to the promotion layout
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
        # Set up logging for user logout
        logging.basicConfig(
        filename="logging_file.txt",
        level=logging.INFO,
        format='%(asctime)s - USER LOGGED OUT'
    )

        logger = logging.getLogger()
        logger.info('')
        exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = PromotionsApp()
    sys.exit(app.exec_())