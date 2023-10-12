# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
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
        self.main_box.setStyleSheet("background-color:rgb(32, 176, 124);\n"
                                     "border-radius: 10px")
        self.main_box.setText("")
        self.main_box.setObjectName("main_box")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 241, 151))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("C:\\Users\\cgatt\\Desktop\\Semister1\\CT4029 - Principles of Programming\\Assigment\\Ass-2049\\UI Files\\../images/Logo.png"))
        self.logo.setObjectName("logo")
        self.email_address = QtWidgets.QLineEdit(self.centralwidget)
        self.email_address.setGeometry(QtCore.QRect(11, 171, 241, 27))
        self.email_address.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                        "border: 1px solid rgba(0, 0, 0, 0);\n"
                                        "border-bottom-color: rgba(0, 0, 0, 255);\n"
                                        "padding-bottom: 7px;\n"
                                        "color: rgb(175, 44, 116);")
        self.email_address.setText("")
        self.email_address.setCursorPosition(0)
        self.email_address.setObjectName("email_address")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(11, 205, 241, 27))
        self.password.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "border: 1px solid rgba(0, 0, 0, 0);\n"
                                   "border-bottom-color: rgba(0, 0, 0, 255);\n"
                                   "padding-bottom: 7px;\n"
                                   "color: rgb(175, 44, 116);")
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.first_name = QtWidgets.QLineEdit(self.centralwidget)
        self.first_name.setGeometry(QtCore.QRect(11, 239, 108, 27))
        self.first_name.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                              "border: 1px solid rgba(0, 0, 0, 0);\n"
                              "border-bottom-color: rgba(0, 0, 0, 255);\n"
                              "padding-bottom: 7px;\n"
                              "color: rgb(175, 44, 116);")
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
                                "color: rgb(175, 44, 116);")
        self.last_name.setInputMask("")
        self.last_name.setText("")
        self.last_name.setMaxLength(255)
        self.last_name.setClearButtonEnabled(False)
        self.last_name.setObjectName("opt_2")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(11, 273, 108, 31))
        self.dateEdit.setObjectName("dateEdit")
        self.confirmation_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirmation_button.setGeometry(QtCore.QRect(126, 273, 126, 28))
        self.confirmation_button.setStyleSheet("border-radius: 5px;\n"
                                              "color: rgb(175, 44, 116);\n"
                                              "background-color: rgb(252, 244, 245)")
        self.confirmation_button.setCheckable(False)
        self.confirmation_button.setObjectName("confirmation_button")
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
