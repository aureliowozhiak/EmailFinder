import sqlite3
import os

def create_database():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            used BOOLEAN DEFAULT FALSE
        )
    ''')
    
    conn.commit()
    return conn, cursor

def insert_email(cursor, email):
    try:
        cursor.execute('INSERT INTO emails (email) VALUES (?)', (email,))
        return True
    except sqlite3.IntegrityError:
        # Email already exists
        return False

def load_emails_to_db():
    """Load emails from file to database and return number of new emails added"""
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    emails_file = os.path.join(current_dir, 'emails.txt')
    
    if not os.path.exists(emails_file):
        print("emails.txt not found")
        return 0
        
    conn, cursor = create_database()
    
    new_emails = 0
    with open(emails_file, 'r', encoding='utf-8') as f:
        for line in f:
            email = line.strip()
            if email and insert_email(cursor, email):
                new_emails += 1
    
    conn.commit()
    conn.close()
    return new_emails

if __name__ == "__main__":
    load_emails_to_db()
