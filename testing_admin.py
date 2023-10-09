import sqlite3

# Function to connect to an existing SQLite database
def connect_to_database(database_name):
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except sqlite3.Error as e:
        print("Error connecting to the database:", str(e))
        return None

# Function to execute a query and fetch results
def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error executing query:", str(e))
        return []

# Function to insert data into the database
def insert_data(conn, table_name, columns, values):
    try:
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        print("Data inserted successfully.")
    except sqlite3.Error as e:
        print("Error inserting data:", str(e))

# Function to update data in the database
def update_data(conn, table_name, set_clause, where_clause):
    try:
        cursor = conn.cursor()
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        cursor.execute(query)
        conn.commit()
        print("Data updated successfully.")
    except sqlite3.Error as e:
        print("Error updating data:", str(e))

# Function to delete data from the database
def delete_data(conn, table_name, where_clause):
    try:
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        cursor.execute(query)
        conn.commit()
        print("Data deleted successfully.")
    except sqlite3.Error as e:
        print("Error deleting data:", str(e))

# Example usage:
if __name__ == "__main__":
    database_name = "promotions.db"
    conn = connect_to_database(database_name)

    if conn:
        while True:
            print("\nOptions:")
            print("1. Execute a query")
            print("2. Insert data")
            print("3. Update data")
            print("4. Delete data")
            print("5. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                query = input("Enter SQL query: ")
                results = execute_query(conn, query)
                for row in results:
                    print(row)
            elif choice == "2":
                table_name = input("Enter table name: ")
                columns = input("Enter columns (comma-separated): ").split(", ")
                values = input("Enter values (comma-separated): ").split(", ")
                insert_data(conn, table_name, columns, values)
            elif choice == "3":
                table_name = input("Enter table name: ")
                set_clause = input("Enter SET clause: ")
                where_clause = input("Enter WHERE clause: ")
                update_data(conn, table_name, set_clause, where_clause)
            elif choice == "4":
                table_name = input("Enter table name: ")
                where_clause = input("Enter WHERE clause: ")
                delete_data(conn, table_name, where_clause)
            elif choice == "5":
                conn.close()
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please try again.")
