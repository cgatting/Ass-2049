import sqlite3

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
        DOB TEXT,
        Last_Login_time TIMESTAMP,
        Last_Login_IP TEXT,
        Last_Logout_OUT TIMESTAMP,
        LAST_SESSION_TIME TIMESTAMP
    )
''')

# Insert sample data into the table
sample_data = [
    ('example1@email.com', 'password1', 'John', 'Doe', '1990-01-15', '2023-10-11 08:00:00', '192.168.1.1', '2023-10-11 17:30:00', '01:30:00'),
    ('example2@email.com', 'password2', 'Jane', 'Smith', '1985-05-20', '2023-10-10 14:45:00', '192.168.1.2', '2023-10-10 22:15:00', '01:45:00'),
]

cursor.executemany('''
    INSERT INTO users
    (email, password, FirstName, LastName, DOB, Last_Login_time, Last_Login_IP, Last_Logout_OUT, LAST_SESSION_TIME)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', sample_data)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Sample data added to the table.")
