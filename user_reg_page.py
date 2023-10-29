# Import necessary modules and libraries
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow
from hashlib import md5
import sys
import sqlite3
import datetime
from user_login_page import user_login

# Define a class for the user registration window
class user_reg(QMainWindow):
    # Function to open the user login window after successful registration
    def go_to_user_login(self, Mainwindow):
        registration_successful = self.user_register()
        if registration_successful:
            self.user_login_window = user_login(Mainwindow) # Create an instance of the user_login window
    # Function to display a success message after registration
    def registration_success(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Registration Successful")
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

    # Function to display a registration failure message
    def registration_failed_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Registration Failed")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        
    def error_invalid_username(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("This is not a valid email address")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        
    # Calculate age based on the date of birth
    def calculate_age(self, dob):
        today = datetime.date.today()
        birth_date = dob.toPyDate()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    # Function to handle user registration
    def user_register(self):
        username = self.email_address.text()
        password = self.password.text()
        first_name = self.first_name.text()
        last_name = self.last_name.text()
        DoB = self.dateEdit.date()

        # Check if any of the required fields are empty
        if not (username and password and first_name and last_name and DoB.isValid()):
            self.error_empty()
            return False

        # Connect to the SQLite database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        FirstName TEXT,
        LastName TEXT,
        DoB DATE
    )
''')
        # Check if the username is already taken
        c.execute("SELECT COUNT(*) FROM users WHERE email=?", (username,))
        if c.fetchone()[0] > 0:
            conn.close()
            self.error_username_taken()
            return False

        # Calculate age from DoB
        age = self.calculate_age(DoB)
        # Check if the user is 18 or older
        if age < 18:
            conn.close()
            self.error_age_too_young()
            return False
        if "@" not in username:
            self.error_invalid_username()
            return False
        # Insert user data into the database
        c.execute("INSERT INTO users (email, password, FirstName, LastName, DoB) VALUES(?,?,?,?,?)",
                  (username, md5(password.encode()).hexdigest(), first_name, last_name, DoB.toString("yyyy-MM-dd")))
        conn.commit()
        conn.close()
        self.registration_success()
        return True

    # Function to display an error message for empty fields
    def error_empty(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You need to enter a username and password")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

    # Function to display an error message for a username that's already taken
    def error_username_taken(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Username is already taken")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

    # Function to display an error message for users under 18
    def error_age_too_young(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You must be 18 or older to register.")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

    # Function to set up the user registration window's UI
    def __init__(self, MainWindow):
        super().__init__()
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
        self.logo.setPixmap(QtGui.QPixmap(r"C:\Users\Clayton\Desktop\Semister1\CT4029 - Principles of Programming\Assigment\Ass-2049\logo.png"))
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
        self.confirmation_button.clicked.connect(lambda: self.go_to_user_login(MainWindow))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)

    # Function to translate UI elements (not provided in the code)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.email_address.setPlaceholderText(_translate("MainWindow", "Email Address"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.first_name.setPlaceholderText(_translate("MainWindow", "First Name"))
        self.last_name.setPlaceholderText(_translate("MainWindow", "Last Name"))
        self.confirmation_button.setText(_translate("MainWindow", "Confirm Registration"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = user_reg(MainWindow)
    ui.__init__(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())