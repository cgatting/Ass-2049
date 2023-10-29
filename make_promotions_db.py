import sqlite3
from datetime import datetime

# Create or connect to the SQLite database
conn = sqlite3.connect('promotions.db')
cursor = conn.cursor()

# Create the Promotions table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Promotions (
        ID INTEGER PRIMARY KEY,
        CouponCode TEXT,
        Description TEXT,
        StartDateTime DATETIME,
        EndDateTime DATETIME,
        BusinessName TEXT
    )
''')

# Insert demo data with date and time
# Commit the changes and close the connection
conn.commit()
conn.close()
