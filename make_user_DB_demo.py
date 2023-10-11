import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('business.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the "promotions" table (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Businesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        Name TEXT
    )
''')

# Insert sample data into the table
sample_data = [
    ('example1@email.com', 'password1', 'John Lewis')
]

cursor.executemany('''
    INSERT INTO businesses
    (email, password, Name)
    VALUES (?, ?, ?)
''', sample_data)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Sample data added to the table.")
