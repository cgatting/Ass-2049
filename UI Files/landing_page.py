# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\cgatt\Desktop\Semister1\CT4029 - Principles of Programming\Assigment\Ass-2049\UI Files\landing_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(306, 479)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_page = QtWidgets.QLabel(self.centralwidget)
        self.main_page.setGeometry(QtCore.QRect(0, 0, 290, 410))
        self.main_page.setStyleSheet("background-color:rgba(32, 176, 124, 255);\n"
"border-radius: 10px")
        self.main_page.setText("")
        self.main_page.setObjectName("main_page")
        self.user_login_button = QtWidgets.QPushButton(self.centralwidget)
        self.user_login_button.setGeometry(QtCore.QRect(20, 200, 116, 28))
        self.user_login_button.setStyleSheet("color: rgb(175, 44, 116);\n"
"background-color: rgb(252, 246, 245);\n"
"border-radius: 5px")
        self.user_login_button.setObjectName("user_login_button")
        self.buiss_login_button = QtWidgets.QPushButton(self.centralwidget)
        self.buiss_login_button.setGeometry(QtCore.QRect(20, 240, 241, 28))
        self.buiss_login_button.setStyleSheet("color: rgb(175, 44, 116);\n"
"background-color: rgb(252, 246, 245);\n"
"border-radius: 5px")
        self.buiss_login_button.setObjectName("buiss_login_button")
        self.user_reg_button = QtWidgets.QPushButton(self.centralwidget)
        self.user_reg_button.setGeometry(QtCore.QRect(140, 200, 116, 28))
        self.user_reg_button.setStyleSheet("color: rgb(175, 44, 116);\n"
"background-color: rgb(252, 246, 245);\n"
"border-radius: 5px")
        self.user_reg_button.setObjectName("user_reg_button")
        self.terms_button = QtWidgets.QPushButton(self.centralwidget)
        self.terms_button.setGeometry(QtCore.QRect(20, 280, 116, 28))
        self.terms_button.setStyleSheet("color: rgb(175, 44, 116);\n"
"background-color: rgb(252, 246, 245);\n"
"border-radius: 5px")
        self.terms_button.setObjectName("terms_button")
        self.conact_button = QtWidgets.QPushButton(self.centralwidget)
        self.conact_button.setGeometry(QtCore.QRect(140, 280, 116, 28))
        self.conact_button.setStyleSheet("color: rgb(175, 44, 116);\n"
"background-color: rgb(252, 246, 245);\n"
"border-radius: 5px")
        self.conact_button.setObjectName("conact_button")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(0, 0, 290, 181))
        self.logo.setText("")
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.user_login_button.setText(_translate("MainWindow", "User Login"))
        self.buiss_login_button.setText(_translate("MainWindow", "Business Login"))
        self.user_reg_button.setText(_translate("MainWindow", "User Register"))
        self.terms_button.setText(_translate("MainWindow", "Terms Contracts"))
        self.conact_button.setText(_translate("MainWindow", "Contact Us"))
