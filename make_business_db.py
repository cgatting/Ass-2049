import sqlite3

# Create or connect to a SQLite database
conn = sqlite3.connect('business.db')
cursor = conn.cursor()

# Create a table to store accounts with an auto-incrementing primary key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        ID INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        business_name TEXT
    )
''')

# Sample data for three demo accounts (excluding the 'id' field)
demo_accounts = [
    ('user1@example.com', 'password1', 'Business 1'),
    ('user2@example.com', 'password2', 'Business 2'),
    ('user3@example.com', 'password3', 'BMW'),
    ('user10@example.com', 'password10', 'BMW')

]

# Insert the demo accounts into the database without specifying the 'id' field
cursor.executemany('INSERT INTO accounts (email, password, business_name) VALUES (?, ?, ?)', demo_accounts)

# Commit the changes and close the database connection
conn.commit()
conn.close()
