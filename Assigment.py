import csv
import sqlite3
import os
# Function to create a CSV file with dummy data
def create_csv(csv_file):
    header = ['name', 'email', 'phone1', 'phone2']
    data = [
        ('John Doe', 'john.doe@example.com', '123-456-7890', '987-654-3210'),
        ('Jane Smith', 'jane.smith@example.com', '555-123-4567', '789-012-3456'),
        ('Arnav', 'arnavsrivastava2001@gmail.com', '8400163158', '789-012-3456')
    ]
    with open(csv_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(data)

# Function to insert records into SQLite database from CSV
def insert_records(csv_file, cursor):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  
        for row in csv_reader:
            name, email, phone1, phone2 = row
            cursor.execute('''
                INSERT INTO phone_book (name, email, phone1, phone2)
                VALUES (?, ?, ?, ?)
            ''', (name, email, phone1, phone2))

# Function to create SQLite table for phone book records
def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phone_book (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone1 TEXT,
            phone2 TEXT
        )
    ''')

# print function
def print_csv_records(csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read and skip the header
        print(f"CSV File Header: {header}")

        print("Records in CSV file:")
        for row in csv_reader:
            print(row)

def update_csv_after_delete(csv_file, name_to_delete):
    temp_csv_file = 'temp.csv'
    
    # Read existing CSV data and create a temporary file
    with open(csv_file, 'r') as file, open(temp_csv_file, 'w', newline='') as temp_file:
        csv_reader = csv.reader(file)
        csv_writer = csv.writer(temp_file)
        header = next(csv_reader)  # Read and skip the header

        # Write header to the temporary file
        csv_writer.writerow(header)

        # Write rows to the temporary file excluding the row to be deleted
        found = False
        for row in csv_reader:
            if row[0] != name_to_delete:
                csv_writer.writerow(row)
            else:
                found = True

    # Replace the original CSV file with the temporary file only if the name was found
    if found:
        os.replace(temp_csv_file, csv_file)
    else:
        print(f"Error: Name '{name_to_delete}' not found in CSV file.")

# Function to run SQL queries and display results
def run_queries(cursor, csv_file):
    queries = [
        'SELECT * FROM phone_book',
        'SELECT * FROM phone_book WHERE name="Arnav"',
        'DELETE FROM phone_book WHERE name="Arnav"'
    ]

    for query in queries:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"Query: {query}")
        for row in results:
            print(row)
        print()

        # Update CSV file after DELETE query
        if 'DELETE' in query:
            name_to_delete = 'Arnav' 
            update_csv_after_delete(csv_file, name_to_delete)

# Function to insert a new record into SQLite database and CSV file
def insert_new_record(cursor, csv_file):
    try:
        name = input("Enter name: ")
        if not all(char.isalpha() or char.isspace() for char in name):
            raise ValueError("Invalid name. Name should only contain alphabetic characters.")

        email = input("Enter email: ")
        phone1 = int(input("Enter phone1: "))
        phone2 = int(input("Enter phone2: "))

        # Execute INSERT query in SQLite database
        cursor.execute('''
            INSERT INTO phone_book (name, email, phone1, phone2)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone1, phone2))

        # Append the new record to the CSV file
        with open(csv_file, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([name, email, str(phone1), str(phone2)])

    except ValueError as e:
        print(f"Error: {e}")
        # Raise the exception again to ensure it is propagated
        raise e



# Main function to execute the program
def main():
    csv_file = 'phone_record.csv'
    database_file = 'phone_database.db'

    # Connect to SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Create the phone_book table
    create_table(cursor)

    # Create CSV file and insert records into the database
    create_csv(csv_file)
    insert_records(csv_file, cursor)

    # Run SQL queries and display results
    run_queries(cursor, csv_file)

    # Insert a new record
    insert_new_record(cursor, csv_file)

    print_csv_records(csv_file)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__== "__main__":
    main()
