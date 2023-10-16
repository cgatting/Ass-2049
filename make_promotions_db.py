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
promotions_data = [
    (1, 'SUMMER20', 'Summer Sale', '2023-06-01 08:00:00', '2023-08-31 20:00:00', 'Example Business A'),
    (2, 'FALL15', 'Fall Discount', '2023-09-01 10:00:00', '2023-11-30 18:00:00', 'Example Business B'),
    (3, 'HOLIDAY25', 'Holiday Promotion', '2023-12-01 09:00:00', '2023-12-31 17:00:00', 'Example Business C')
]

cursor.executemany('''
    INSERT INTO Promotions (ID, CouponCode, Description, StartDateTime, EndDateTime, BusinessName)
    VALUES (?, ?, ?, ?, ?, ?)
''', promotions_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
