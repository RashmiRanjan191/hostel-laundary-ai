import sqlite3

def init_db():
    conn = sqlite3.connect('hostel_laundry.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (roll_no TEXT PRIMARY KEY, name TEXT, password TEXT, usage_count INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def register_user(roll_no, name, password):
    conn = sqlite3.connect('hostel_laundry.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (roll_no, name, password, usage_count) VALUES (?, ?, ?, 0)", 
                  (roll_no, name, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(roll_no, password):
    conn = sqlite3.connect('hostel_laundry.db')
    c = conn.cursor()
    c.execute("SELECT name, usage_count FROM users WHERE roll_no = ? AND password = ?", (roll_no, password))
    user = c.fetchone()
    conn.close()
    return user

def increment_usage(roll_no):
    conn = sqlite3.connect('hostel_laundry.db')
    c = conn.cursor()
    c.execute("UPDATE users SET usage_count = usage_count + 1 WHERE roll_no = ?", (roll_no,))
    conn.commit()
    conn.close()

def get_all_usage():
    conn = sqlite3.connect('hostel_laundry.db')
    c = conn.cursor()
    c.execute("SELECT roll_no, name, usage_count FROM users")
    data = c.fetchall()
    conn.close()
    return data
def delete_user_account(roll_no):
    """Permanently removes the user from the database so they can re-register."""
    conn = sqlite3.connect('hostel_laundry.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE roll_no = ?", (roll_no,))
    conn.commit()
    conn.close()