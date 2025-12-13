"""
Quick script to create a default admin account for SQLite
Default credentials:
Username: admin
Password: admin123
"""
from werkzeug.security import generate_password_hash
import sqlite3
import os

# Get absolute path to the database file (one level up from this script)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, 'database', 'bank_db.db')

def create_default_admin():
    """Create a default admin account"""
    username = "admin"
    password = "admin123"
    full_name = "System Administrator"
    
    try:
        # Check if database exists
        if not os.path.exists(DATABASE):
            print("[!] Database not found! Please run app.py first to create the database.")
            return
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT * FROM admins WHERE username=?", (username,))
        existing = cursor.fetchone()
        if existing:
            print(f"\n[!] Admin account '{username}' already exists!")
            print("You can use the existing account or create a new one with create_admin.py")
            conn.close()
            return
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Insert admin
        cursor.execute(
            "INSERT INTO admins (username, password, full_name) VALUES (?, ?, ?)",
            (username, hashed_password, full_name)
        )
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 50)
        print("[OK] Default Admin Account Created Successfully!")
        print("=" * 50)
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Full Name: {full_name}")
        print("\n[!] IMPORTANT: Change the password after first login!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n[X] Error: {str(e)}")
        print("\nPlease check:")
        print("  1. Database file exists (run app.py first)")
        print("  2. Database is not locked by another process")

if __name__ == "__main__":
    create_default_admin()
