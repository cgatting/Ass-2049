import sqlite3
import datetime

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the "promotions" table (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        FirstName TEXT,
        LastName TEXT,
        DoB DATETIME
    )
''')

# Insert sample data into the table
sample_data = [
    ('Admin@GRL.com', 'Admin1.', 'Admin', "Admin", datetime.datetime(1990, 1, 1))
]

cursor.executemany('''
    INSERT INTO users
    (email, password, FirstName, LastName, DoB)
    VALUES (?, ?, ?, ?, ?)
''', sample_data)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Sample data added to the table.")
