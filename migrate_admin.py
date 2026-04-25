
import sqlite3
import os

DB_PATH = os.path.join("instance", "jobmatch.db")

def add_admin_column():
    """Adds is_admin column to user table if it doesn't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'is_admin' not in columns:
            print("Adding is_admin column...")
            cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column is_admin already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Error migrating database: {e}")

def promote_user(email):
    """Promotes a user to admin"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE user SET is_admin = 1 WHERE email = ?", (email,))
        if cursor.rowcount > 0:
            print(f"User {email} promoted to ADMIN.")
            conn.commit()
        else:
            print(f"User {email} not found.")
            
        conn.close()
    except Exception as e:
        print(f"Error promoting user: {e}")

def list_users():
    """Lists all users to help select admin"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, email, is_admin FROM user")
        users = cursor.fetchall()
        
        print("\nExisting Users:")
        print(f"{'ID':<5} {'Email':<30} {'Is Admin':<10}")
        print("-" * 50)
        for u in users:
            is_adm = "YES" if u[2] else "NO"
            print(f"{u[0]:<5} {u[1]:<30} {is_adm:<10}")
        print("-" * 50)
            
        conn.close()
    except Exception as e:
        print(f"Error listing users: {e}")

if __name__ == "__main__":
    add_admin_column()
    list_users()
    
    val = input("\nEnter email to promote to Admin (or press Enter to skip): ").strip()
    if val:
        promote_user(val)
