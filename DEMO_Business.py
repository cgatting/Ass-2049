import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from business_management import BusinessMainPage
import sqlite3
class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.login_button = QPushButton("Login")

        self.login_button.clicked.connect(self.login)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.central_widget.setLayout(self.layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        conn = sqlite3.connect("business.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE email=? AND password=?", (username, password))
        user = cursor.fetchone()
        print(user[1], user[2])
        if user is None:
            self.show_error_message("Invalid username or password")
        if user[1] == username and user[2] == password:
            self.show_success_message("Login successful")
            self.open_business_main_page()
        return user

    def open_business_main_page(self):
        self.business_main_page = BusinessMainPage()
        self.business_main_page.show()
        self.close()

    def show_success_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.exec_()

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_app = LoginPage()
    login_app.show()
    sys.exit(app.exec_())
