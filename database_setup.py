import sqlite3

DATABASE_NAME = 'patients.db'

def create_table():
    conn = sqlite3.connect(DATABASE_NAME) 
    cursor = conn.cursor() 

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL, -- Stored as 'YYYY-MM-DD'
            phone_number TEXT NOT NULL
        )
    ''')
    conn.commit() 
    conn.close() 

def add_patient(first_name, last_name, dob, phone_number):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
   
    cursor.execute('''
        INSERT INTO patients (first_name, last_name, dob, phone_number)
        VALUES (?, ?, ?, ?)
    ''', (first_name.lower(), last_name.lower(), dob, phone_number)) 
    conn.commit()
    conn.close()
    print(f"Added patient: {first_name} {last_name}")

if __name__ == '__main__':
    create_table() 
    add_patient('John', 'Doe', '1990-01-01', '1234567890')
    add_patient('Jane', 'Smith', '1985-03-15', '0987654321')
    add_patient('Alice', 'Wonderland', '2000-07-22', '5551234567')
    print("Database and mock data created successfully!")