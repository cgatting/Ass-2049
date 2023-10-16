import sqlite3
import getpass
import hashlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton, QLineEdit, QLabel, QDialog, QDialogButtonBox, QMessageBox, QTableWidgetItem

class AdminPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Admin")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.table_widget.setStyleSheet("background-color: #F5F7F7; color: #000407")

        self.database_name = None
        self.table_name = None

        self.database_buttons = self.create_database_buttons()
        self.edit_button = self.create_button("Edit Item", self.edit_item)
        self.add_button = self.create_button("Add Item", self.add_data)
        self.delete_button = self.create_button("Remove Items", self.delete_item)
        self.search_input = self.create_search_input()
        self.central_widget.setLayout(self.layout)

        self.conn = None
        self.cursor = None
        self.data = []

    def search_data(self, search_text):
        search_text = self.search_input.text()
        if not self.database_name or not self.table_name:
            return

        cursor = self.cursor

        # Fetch column names
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        column_names = [row[1] for row in cursor.fetchall()]

        self.table_widget.setRowCount(0)  # Clear existing rows

        # Construct the SQL query for searching
        query = f"SELECT * FROM {self.table_name} WHERE {column_names[0]} LIKE ?"
        for column in column_names[1:]:
            query += f" OR {column} LIKE ?"

        search_text = f"%{search_text}%"  # Add wildcards for a partial match

        cursor.execute(query, tuple([search_text] * len(column_names)))
        search_results = cursor.fetchall()

        for row_num, row_data in enumerate(search_results):
            self.table_widget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table_widget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    def create_button(self, text, on_click):
        button = QPushButton(text)
        button.clicked.connect(on_click)
        self.layout.addWidget(button)
        button.setStyleSheet("background-color: #000407; color: white;")
        return button

    def create_search_input(self):
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search")
        self.layout.addWidget(search_input)
        return search_input

    def create_database_buttons(self):
        database_buttons = QWidget(self)
        database_layout = QVBoxLayout()
        self.user_button = self.create_button("Users Database", lambda: self.select_table('users', 'users'))
        self.promotion_button = self.create_button("Promotions Database", lambda: self.select_table('promotions', 'promotions'))
        self.business_login = self.create_button("Business Accounts Database", lambda: self.select_table('business', 'accounts'))

        database_layout.addWidget(self.user_button)
        database_layout.addWidget(self.promotion_button)
        database_layout.addWidget(self.business_login)
        database_buttons.setLayout(database_layout)
        self.layout.addWidget(database_buttons)

    def select_table(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name
        self.conn = sqlite3.connect(f'{database_name}.db')
        self.cursor = self.conn.cursor()
        self.load_data()

    def load_data(self):
        self.load_table_data(self.database_name, self.table_name)

    def load_table_data(self, database_name, table_name):
        self.table_widget.clear()
        self.table_widget.setRowCount(0)

        cursor = self.cursor

        # Fetch column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        column_names = [row[1] for row in cursor.fetchall()]

        self.table_widget.setColumnCount(len(column_names))
        self.table_widget.setHorizontalHeaderLabels(column_names)

        cursor.execute(f"SELECT * FROM {table_name}")
        self.data = cursor.fetchall()

        for row_num, row_data in enumerate(self.data):
            self.table_widget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table_widget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    def edit_item(self):
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

        cursor = self.cursor

        # Fetch the existing data for the selected item
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE ID = ?", (item_id,))
        item_data = cursor.fetchone()

        if item_data is None:
            return

        # Create input fields for each column in the table, excluding 'ID' and 'password'
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        column_names = [row[1] for row in cursor.fetchall()]

        # Remove 'ID' and 'password' from column_names
        column_names.remove('ID')

        input_fields = {}
        for column, value in zip(column_names, item_data[1:]):  # Start from 1 to skip 'ID'
            if column != "ID" and column!= 'password':
                label = QLabel(f"{column}:")
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
            # Get edited values from input fields for columns that are not "password" or "ID"
            edited_values = [input_fields[column].text() for column in column_names if column not in ["password", "ID"]]

            # Create an SQL query to update the data
            set_values = ', '.join([f"{column} = ?" for column in column_names if column not in ["password", "ID"]])
            update_query = f"UPDATE {self.table_name} SET {set_values} WHERE ID = ?"
            edited_values.append(item_id)  # Append the item_id to update the correct row

            # Use parameterized query to update the data, avoiding SQL injection
            cursor.execute(update_query, edited_values)
            self.conn.commit()

            # Refresh the table data
            self.load_data()

    def add_data(self):
        if not self.database_name or not self.table_name:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Item")
        dialog_layout = QVBoxLayout()

        # Create input fields for each column in the table
        cursor = self.cursor
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        column_names = [row[1] for row in cursor.fetchall()]

        # Remove 'ID' from column_names
        column_names.remove('ID')

        # Input fields for other columns
        input_fields = {}
        for column in column_names:
            label = QLabel(f"{column}:")
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
            # Get values from input fields, including the password
            values = [input_fields[column].text() for column in column_names]

            # Encrypt the password with MD5
            password = input_fields["password"].text()
            md5_password = hashlib.md5(password.encode()).hexdigest()
            values.append(md5_password)
            print(values)
            # Insert the new data into the table
            cursor.execute(f"INSERT INTO {self.table_name} ({', '.join(column_names)}) VALUES ({', '.join(['?'] * (len(column_names)))}", values)
            self.conn.commit()

            # Refresh the table data
            self.load_data()

    def delete_item(self):
        if not self.database_name or not self.table_name:
            return

        # Ensure a row is selected for deletion
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        # Get the row number of the selected item
        row = selected_items[0].row()

        # Retrieve the item_id from the data list (assuming the ID is in the first column)
        item_id = self.data[row][0]

        # Ensure the user confirms the deletion
        confirm = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this item?', QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            cursor = self.cursor

            # Delete the selected item from the table
            cursor.execute(f"DELETE FROM {self.table_name} WHERE ID = ?", (item_id,))
            self.conn.commit()

            # Remove the selected item's row from the QTableWidget
            self.table_widget.removeRow(row)

if __name__ == "__main__":
    app = QApplication([])
    window = AdminPage()
    window.show()
    app.exec()
