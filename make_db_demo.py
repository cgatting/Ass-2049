import sqlite3

# Create or connect to the database file
conn = sqlite3.connect("promotions.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define sample data to be inserted
sample_data = [
    ("Promotion 1", "Voucher1"),
    ("Promotion 2", "Voucher2"),
    ("Promotion 3", "Voucher3")
]
cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                voucher_code TEXT
            )
        ''')

# Insert sample data into the "promotions" table
for data in sample_data:
    cursor.execute("INSERT INTO promotions (text, voucher_code) VALUES (?, ?)", data)

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Sample data added to the 'promotions' table.")
