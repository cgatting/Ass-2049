import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
from PyQt5.QtGui import QPalette, QColor

class AdminPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Database Admin")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.table_widget.setStyleSheet("background-color: #F5F7F7; color: #000407")

        self.load_data_button = self.create_button("Load Data", self.load_data)
        self.edit_button = self.create_button("Edit Selected", self.edit_selected)
        self.add_button = self.create_button("Add User", self.add_user)
        self.search_input = self.create_search_input()
        self.search_button = self.create_button("Search", self.search_data)
        self.user_management_button = self.create_button("User Management", self.open_user_management)

        self.central_widget.setLayout(self.layout)

        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.data = []

    def create_button(self, text, on_click):
        button = QPushButton(text)
        button.clicked.connect(on_click)
        self.layout.addWidget(button)
        button.setStyleSheet("background-color: #000407; color: white;")
        return button

    def create_search_input(self):
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search Username")
        self.layout.addWidget(search_input)
        return search_input

    def load_data(self):
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Username", "Password"])

        self.cursor.execute("SELECT * FROM users")
        self.data = self.cursor.fetchall()

        for row_num, row_data in enumerate(self.data):
            self.table_widget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table_widget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    def edit_selected(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        user_id = self.data[row][0]
        self.edit_user_dialog(user_id)

    def edit_user_dialog(self, user_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User")
        dialog_layout = QVBoxLayout()
        user_data = self.get_user_data(user_id)
        if user_data is None:
            return
        id_label = QLabel("ID:")
        id_label_value = QLabel(str(user_data[0]))
        dialog_layout.addWidget(id_label)
        dialog_layout.addWidget(id_label_value)
        username_input = self.create_input_field("Username", user_data[1])
        password_input = self.create_input_field("Password", user_data[2])
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, parent=dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(username_input)
        dialog_layout.addWidget(password_input)
        dialog_layout.addWidget(buttons)
        dialog.setLayout(dialog_layout)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            new_username = username_input.text()
            new_password = password_input.text()
            self.update_user_data(user_id, new_username, new_password)
            self.load_data()

    def create_input_field(self, label_text, default_value=""):
        label = QLabel(label_text + ":")
        input_field = QLineEdit()
        input_field.setText(default_value)
        return input_field

    def get_user_data(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE ID = ?", (user_id,))
        user_data = self.cursor.fetchone()
        return user_data

    def update_user_data(self, user_id, new_username, new_password):
        self.cursor.execute("UPDATE users SET username = ?, password = ? WHERE ID = ?", (new_username, new_password, user_id))
        self.conn.commit()

    def add_user(self):
        self.add_user_dialog()

    def add_user_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add User")
        dialog_layout = QVBoxLayout()
        username_input = self.create_input_field("Username")
        password_input = self.create_input_field("Password")
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, parent=dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(username_input)
        dialog_layout.addWidget(password_input)
        dialog_layout.addWidget(buttons)
        dialog.setLayout(dialog_layout)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.insert_new_user(username_input.text(), password_input.text())
            self.load_data()

    def insert_new_user(self, username, password):
        self.cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def search_data(self):
        search_text = self.search_input.text()
        if not search_text:
            return
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Username", "Password"])
        self.cursor.execute("SELECT * FROM users WHERE username LIKE ?", ('%' + search_text + '%',))
        search_results = self.cursor.fetchall()
        for row_num, row_data in enumerate(search_results):
            self.table_widget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table_widget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    def open_user_management(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPage()
    window.show()
    sys.exit(app.exec_())
