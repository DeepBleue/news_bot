import sqlite3
def create_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS numbers 
                      (id INTEGER PRIMARY KEY, number TEXT UNIQUE)''')
    conn.commit()
    conn.close()

# Function to insert a new number into the database
def insert_number(number,db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO numbers (number) VALUES (?)", (number,))
        conn.commit()
    except sqlite3.IntegrityError:  # This happens if the number is already in the database
        pass
    conn.close()

# Function to check if a number is already in the database
def number_exists(number,db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM numbers WHERE number = ?", (number,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def delete_id(db_name, id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM numbers WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def get_id_to_delete(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Assuming 'id' is your primary key and you want to delete the most recent entry
    cursor.execute("SELECT id FROM numbers ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else None
