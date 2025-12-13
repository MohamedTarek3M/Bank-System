"""
Interactive script to create an admin account for SQLite
"""
from werkzeug.security import generate_password_hash
import sqlite3
import os

# Get absolute path to the database file (one level up from this script)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, 'database', 'bank_db.db')

def create_admin():
    """Create an admin account"""
    print("=" * 50)
    print("Bank Management System - Admin Account Creator")
    print("=" * 50)
    
    # Check if database exists
    if not os.path.exists(DATABASE):
        print("[!] Database not found! Please run app.py first to create the database.")
        return
    
    username = input("Enter admin username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return
    
    password = input("Enter admin password: ").strip()
    if not password:
        print("Password cannot be empty!")
        return
    
    full_name = input("Enter admin full name: ").strip()
    if not full_name:
        full_name = "Administrator"
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT * FROM admins WHERE username=?", (username,))
        existing = cursor.fetchone()
        if existing:
            print(f"\n[X] Error: Username '{username}' already exists!")
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
        
        print("\n[OK] Admin account created successfully!")
        print(f"   Username: {username}")
        print(f"   Full Name: {full_name}")
        print("\nYou can now login with these credentials.")
        
    except Exception as e:
        print(f"\n[X] Error creating admin account: {str(e)}")
        print("Make sure:")
        print("  1. Database file exists (run app.py first)")
        print("  2. Database is not locked by another process")

if __name__ == "__main__":
    create_admin()
