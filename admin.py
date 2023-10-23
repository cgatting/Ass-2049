import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
    QTableWidgetItem,
    QDateTimeEdit,
)
from PyQt5.QtCore import Qt
import datetime
import random
import smtplib
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import md5

class AdminPage(QMainWindow):
    
    def __init__(self, email):
        super().__init__()
        self.setWindowTitle("Database Admin")
        self.setGeometry(100, 100, 800, 600)

        # Create the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Create a table widget for displaying data
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.table_widget.setStyleSheet("background-color: #F5F7F7; color: #000407")

        # Initialize database and table names
        self.database_name = None
        self.table_name = None

        # Create database selection buttons
        self.create_database_buttons()

        # Create action buttons for editing, adding, and deleting data
        self.edit_button = self.create_button("Edit Item", self.edit_item)
        self.add_button = self.create_button("Add Item", self.add_data)
        self.delete_button = self.create_button("Remove Items", self.delete_item)
        self.user_button = self.create_button("Users Database", lambda: self.select_table('users', 'users'))
        self.promotion_button = self.create_button("Promotions Database", lambda: self.select_table('promotions', 'promotions'))
        self.business_login = self.create_button("Business Accounts Database", lambda: self.select_table('business', 'accounts'))

        # Create a search input field
        self.search_input = self.create_search_input()
        self.search_input.textChanged.connect(self.search_data)  # Connect text change event to search

        # Set the layout for the central widget
        self.central_widget.setLayout(self.layout)

        # Initialize database connection and data storage
        self.conn = None
        self.cursor = None
        self.column_names = []
        self.data = []

    def create_button(self, text, on_click):
        # Create a QPushButton with the specified text and click event handler
        button = QPushButton(text)
        button.clicked.connect(on_click)
        self.layout.addWidget(button)
        button.setStyleSheet("background-color: #000407; color: white;")
        return button
    def OTP_Sent_message(self):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("OTP has been sent to your email")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
    def create_search_input(self):
        # Create a search input field with a placeholder text
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search")
        self.layout.addWidget(search_input)
        return search_input

    def create_database_buttons(self):
        database_buttons = QWidget(self)
        database_layout = QVBoxLayout()

        # Create a dictionary that maps button text to database and table names
        # self.database_button_mapping = {
        #     "Users Database": ("users", "users"),
        #     "Promotions Database": ("promotions", "promotions"),
        #     "Business Accounts Database": ("business", "accounts"),
        # }

        # # Create buttons for database selection
        # for text, (database_name, table_name) in self.database_button_mapping.items():
        #     button = self.create_button(text, lambda name=database_name, table=table_name: self.select_table(name, table))
        #     database_layout.addWidget(button)

        database_buttons.setLayout(database_layout)
        self.layout.addWidget(database_buttons)

    def select_table(self, database_name, table_name):
        try:
            self.database_name = database_name
            self.table_name = table_name
            self.conn = sqlite3.connect(f'{database_name}.db')
            self.cursor = self.conn.cursor()
            self.load_data()
        except sqlite3.Error as e:
            print("Database connection error:", e)


    def load_data(self):
        if not self.database_name or not self.table_name:
            return

        # Fetch column names and load table data
        self.column_names = self.fetch_column_names(self.table_name)
        self.load_table_data(self.table_name)

    def fetch_column_names(self, table_name):
        # Retrieve the column names for the specified table
        cursor = self.cursor
        cursor.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in cursor.fetchall()]

    def load_table_data(self, table_name):
        # Load data from the selected table into the table widget
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(len(self.column_names))
        self.table_widget.setHorizontalHeaderLabels(self.column_names)

        cursor = self.cursor
        cursor.execute(f"SELECT * FROM {table_name}")
        self.data = cursor.fetchall()

        self.populate_table(self.data)

    def populate_table(self, data):
        # Populate the table widget with data
        self.table_widget.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row_num, col_num, item)

    def search_data(self):
        # Search for data that matches the search input
        search_text = self.search_input.text()
        if not self.database_name or not self.table_name:
            return

        search_text = f"%{search_text}%"
        query = f"SELECT * FROM {self.table_name} WHERE {' LIKE ? OR '.join(self.column_names)} LIKE ?"
        self.cursor.execute(query, [search_text] * len(self.column_names))
        search_results = self.cursor.fetchall()

        self.populate_table(search_results)

    def edit_item(self):
        # Edit the selected item
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        row = selected_items[0].row()
        item_id = self.data[row][0]
        self.edit_item_dialog(item_id)

    def edit_item_dialog(self, item_id):
        if not self.database_name or not self.table_name:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Item")
        dialog_layout = QVBoxLayout()
        item_data = self.fetch_item_data(item_id)

        if item_data is None:
            return

        input_fields = {}
        for column, value in zip(self.column_names, item_data):  # Start from 1 to skip 'ID'
            if column not in ["ID", "password"]:
                label = QLabel(f"{column}:")
                if "DateTime" in column:
                    input_field = QDateTimeEdit()
                    input_field.setDateTime(datetime.datetime.strptime(value, "%d/%m/%Y %H:%M"))
                else:
                    input_field = QLineEdit()
                    input_field.setText(str(value))
                input_fields[column] = input_field
                dialog_layout.addWidget(label)
                dialog_layout.addWidget(input_field)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, parent=dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(buttons)
        dialog.setLayout(dialog_layout)

        result = dialog.exec_()
        if result == QDialog.Accepted:
            edited_values = [input_fields[column].text() for column in self.column_names if column not in ["ID", "password"]]
            self.update_item(item_id, edited_values)
            self.load_data()
        self.conn.commit()

    def fetch_item_data(self, item_id):
        # Retrieve data for the selected item
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE ID = ?", (item_id,))
        return self.cursor.fetchone()

    def update_item(self, item_id, edited_values):
        # Update the selected item with the edited values
        set_values = ', '.join([f"{column} = ?" for column in self.column_names if column not in ["password", "ID"]])
        update_query = f"UPDATE {self.table_name} SET {set_values} WHERE ID = ?"
        edited_values.append(item_id)
        self.cursor.execute(update_query, edited_values)
        self.conn.commit()

    def add_data(self):
        # Add a new item to the table
        if not self.database_name or not self.table_name:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Item")
        dialog_layout = QVBoxLayout()

        input_fields = {}
        for column in self.column_names:
            if column not in ["ID"]:
                label = QLabel(f"{column}:")
                if "DateTime" in column:
                    input_field = QDateTimeEdit()
                else:
                    input_field = QLineEdit()
                input_fields[column] = input_field
                dialog_layout.addWidget(label)
                dialog_layout.addWidget(input_field)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, parent=dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(buttons)
        dialog.setLayout(dialog_layout)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            values = [input_fields[column].text() for column in self.column_names if column not in ["ID"]]
            self.encrypt_password(values)
            self.format_datetime(values)
            self.insert_data(values)
            self.load_data()

    def encrypt_password(self, values):
        # Encrypt the password using MD5 if there is a 'password' column
        password_column = "password"
        if password_column in self.column_names:
            password_index = self.column_names.index(password_column)-1
            password = values[password_index]
            md5_password = md5(password.encode()).hexdigest()
            values[password_index] = md5_password

    def format_datetime(self, values):
        # Format DateTime columns to a consistent format
        for i, column in enumerate(self.column_names):
            if "DateTime" in column:
                try:
                    values[i] = datetime.datetime.strptime(values[i], "%d/%m/%Y %H:%M").strftime("%Y/%m/%d %H:%M")
                except:
                    pass

    def insert_data(self, values):
        # Insert the new item into the table
        insert_query = f"INSERT INTO {self.table_name} ({', '.join(self.column_names[1:])}) VALUES ({', '.join(['?'] * (len(self.column_names) - 1))})"
        self.cursor.execute(insert_query, values)
        self.conn.commit()
        self.load_data()

    def delete_item(self):
        # Delete the selected item from the table
        if not self.database_name or not self.table_name:
            return

        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        row = selected_items[0].row()
        item_id = self.data[row][0]

        confirm = QMessageBox.question(
            self, 'Confirm Deletion', 'Are you sure you want to delete this item?', QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.cursor.execute(f"DELETE FROM {self.table_name} WHERE ID = ?", (item_id,))
            self.conn.commit()
            self.table_widget.removeRow(row)
    def write_new_business_password(self):
        digit_string = ''.join(random.choice('0123456789') for _ in range(4))
        return digit_string
        
    def password_reset(self):
        email = "cgatting@gmail.com"
        new_password = self.write_new_business_password()
        _translate = QtCore.QCoreApplication.translate
        sender_email = 'cgatting@gmail.com'
        recipient_email = email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'cgatting@gmail.com'
        smtp_password = 'oytu gdvz jnkt uyjh'
        subject = 'Updated Password'
        message = f'Your New Password is is: {new_password}'
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
        conn = sqlite3.connect('business.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET password = ? WHERE email = ?", (md5(new_password.encode()).hexdigest(), email))
        conn.commit()
        conn.close()
        return new_password
        


# if __name__ == "__main__":
#     app = QApplication([])
#     window = AdminPage()
#     window.show()
#     app.exec()

