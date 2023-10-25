import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
import webbrowser

class TermsAndConditionsWindow(QMainWindow):
    def open_email_client(self, text):
        mailto_link = f'mailto:?subject=Terms%20and%20Conditions%20For%20QRLife&body={text}'
        webbrowser.open(mailto_link)
    
    def __init__(self):
        super().__init()

        self.setWindowTitle("Terms and Conditions")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        terms_label = QLabel("Terms and Conditions")
        terms_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(terms_label)

        terms_text = QTextEdit()
        terms_text.setPlainText("""
1. Acceptance of Terms

By accessing or using the [Your App Name] (hereinafter referred to as "the App") developed by [Your Company Name] (hereinafter referred to as "the Company"), you agree to comply with and be bound by the following terms and conditions.

2. Use of the App

2.1. The App is intended for personal and non-commercial use. You may not use the App for any unlawful purpose or in any way that violates applicable UK laws and regulations.

2.2. The Company reserves the right to modify, suspend, or terminate the App's services at any time without prior notice.

3. User Accounts

3.1. To access certain features of the App, you may be required to create a user account. You are responsible for maintaining the confidentiality of your account information and password.

3.2. You must provide accurate and complete information when creating your user account.

4. Privacy and Data Protection

4.1. The Company may collect and process your personal information in accordance with its Privacy Policy, which can be found on the App.

5. Intellectual Property

5.1. The App and its content, including but not limited to text, graphics, images, and software, are protected by copyright and other intellectual property laws. You may not reproduce, modify, distribute, or publicly display any part of the App without the Company's prior written consent.

6. User-Generated Content

6.1. You may be able to submit and share user-generated content through the App. By doing so, you grant the Company a non-exclusive, royalty-free, worldwide license to use, reproduce, and distribute your content.

7. Prohibited Activities

7.1. You are prohibited from engaging in any of the following activities when using the App:

- Violating any applicable laws or regulations.
- Uploading, sharing, or transmitting any harmful or malicious content.
- Harassing, defaming, or discriminating against others.
- Attempting to gain unauthorized access to the App's systems.

8. Limitation of Liability

8.1. The Company makes no warranties or representations about the accuracy or completeness of the App's content. Your use of the App is at your own risk.

8.2. The Company is not liable for any direct, indirect, incidental, special, or consequential damages arising from your use of the App.

9. Termination

9.1. The Company may terminate your access to the App at its discretion if you violate these terms and conditions.

10. Governing Law

10.1. These terms and conditions are governed by and construed in accordance with the laws of England and Wales. Any disputes arising from your use of the App will be subject to the exclusive jurisdiction of the courts of England and Wales.

11. Contact Information

11.1. For questions or concerns regarding these terms and conditions, please contact [Your Company Contact Information].
""")
        layout.addWidget(terms_text)

        accept_button = QPushButton("Accept")
        accept_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        email_button = QPushButton("Send to Email")
        email_button.setStyleSheet("QPushButton{background-color: #000407; color: white;} QPushButton::pressed {background-color: #edb518;}")
        layout.addWidget(accept_button)
        layout.addWidget(email_button)
        accept_button.clicked.connect(self.accept_terms)
        email_button.clicked.connect(lambda: self.open_email_client(terms_text.toPlainText()))

    def accept_terms(self):
        # Handle the acceptance of terms here (e.g., saving the acceptance state to a file or database).
        # You can customize this function according to your application's needs.
        print("Terms accepted")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    terms_window = TermsAndConditionsWindow()
    terms_window.show()
    sys.exit(app.exec_())
