import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QDialog, QDialogButtonBox, QLineEdit, QLabel, QDateTimeEdit
import datetime
import sys
class BusinessMainPage(QMainWindow):
    
    def __init__(self, username):
        def get_business_data():
            conn = sqlite3.connect("business.db")
            cursor = conn.cursor()
            cursor.execute("SELECT business_name FROM accounts WHERE email=?", (username,))
            user = cursor.fetchone()
            conn.close()
            return user
        bus_username = get_business_data()
        super().__init__()
        self.setWindowTitle("Database Admin")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.table_widget.setStyleSheet("background-color: #F5F7F7; color: #000407")

        # Set the database name and table name
        self.database_name = 'promotions.db'
        self.table_name = 'promotions'

        self.central_widget.setLayout(self.layout)

        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()
        self.data = []
        self.bus_username = bus_username  # Business name

        self.load_data()

        # Add an "Edit" button
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_data)
        self.layout.addWidget(self.edit_button)

        # Add an "Add" button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_data)
        self.layout.addWidget(self.add_button)

    def load_data(self):
        self.load_table_data(self.database_name, self.table_name)

    def  load_table_data(self, database_name, table_name):
        self.table_widget.clear()
        self.table_widget.setRowCount(0)

        cursor = self.cursor

        # Fetch column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        column_names = [row[1] for row in cursor.fetchall()]

        self.table_widget.setColumnCount(len(column_names))
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # Select data only for the specified business (using a WHERE clause)
        cursor.execute(f"SELECT * FROM {table_name} WHERE BusinessName = ?", (self.bus_username,))
        self.data = cursor.fetchall()

        for row_num, row_data in enumerate(self.data):
            self.table_widget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table_widget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    def edit_data(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        # Get the row and column of the selected cell
        row = selected_items[0].row()
        col = selected_items[0].column()

        # Get the original data from the cell
        original_data = self.table_widget.item(row, col).text()
        
        # Create a dialog for editing the data
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Data")
        edit_layout = QVBoxLayout()
        print(self.table_widget.horizontalHeaderItem(col).text())
        if self.table_widget.horizontalHeaderItem(col).text() in ["StartDateTime", "EndDateTime"]:
            edit_field = QDateTimeEdit()
            edit_field.setDateTime(datetime.datetime.strptime(original_data, '%Y-%m-%d %H:%M:%S'))
        else:
            edit_field = QLineEdit()
            edit_field.setText(original_data)
        edit_layout.addWidget(edit_field)
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, parent=edit_dialog)
        buttons.accepted.connect(edit_dialog.accept)
        buttons.rejected.connect(edit_dialog.reject)
        edit_layout.addWidget(buttons)

        edit_dialog.setLayout(edit_layout)

        result = edit_dialog.exec_()

        if result == QDialog.Accepted:
            # Update the cell with the edited data
            new_data = edit_field.text()
            self.table_widget.setItem(row, col, QTableWidgetItem(new_data))

            # Save the edited data back to the database
            self.update_database(row, col, new_data)

    def update_database(self, row, col, new_data):
        # Get the primary key (ID) of the selected record
        primary_key = self.data[row][0]

        # Get the column name being edited
        column_name = self.table_widget.horizontalHeaderItem(col).text()

        # Construct an SQL query to update the specific record
        update_query = f"UPDATE {self.table_name} SET {column_name} = ? WHERE ID = ?"

        # Execute the SQL UPDATE statement
        self.cursor.execute(update_query, (new_data, primary_key))
        self.conn.commit()

    def add_data(self):
    # Create a dialog for entering new data
        add_dialog = QDialog(self)
        add_dialog.setWindowTitle("Add Data")
        add_layout = QVBoxLayout()

        # Fetch column names
        cursor = self.cursor
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        column_names = [row[1] for row in cursor.fetchall()]

        # Create input fields for each column
        input_fields = {}
        for column_name in column_names:
            label = QLabel(f"{column_name}:")
            input_field = QLineEdit()
            input_fields[column_name] = input_field
            add_layout.addWidget(label)
            add_layout.addWidget(input_field)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, parent=add_dialog)
        buttons.accepted.connect(add_dialog.accept)
        buttons.rejected.connect(add_dialog.reject)
        add_layout.addWidget(buttons)

        add_dialog.setLayout(add_layout)

        result = add_dialog.exec_()

        if result == QDialog.Accepted:
            # Get the new data from the input fields
            new_data = []
            for column_name in column_names:
                new_data.append(input_fields[column_name].text())

            # Save the new data to the database
            self.save_new_data(new_data)

    def save_new_data(self, new_data):
        # Construct an SQL query to insert the new data into the database
        columns = ', '.join(self.table_widget.horizontalHeaderItem(col).text() for col in range(self.table_widget.columnCount()))
        values = ', '.join(['?'] * self.table_widget.columnCount())

        insert_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"

        # Execute the SQL INSERT statement
        self.cursor.execute(insert_query, new_data)
        self.conn.commit()
        self.load_data()

