import sqlite3
import os
import sys

def migrate_database():
    """Add missing columns to user table if they don't exist"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'jobmatch.db')
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), 'instance', 'jobmaths.db')
    
    if not os.path.exists(db_path):
        print("Database not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        new_columns = [
            ('bio', 'TEXT'),
            ('achievements', 'TEXT'),
            ('skills', 'TEXT')
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in columns:
                print(f"Adding '{col_name}' column...")
                cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} {col_type}")
                print(f"Added {col_name} column successfully")
            else:
                print(f"Column '{col_name}' already exists")
        
        conn.commit()
        print("\nMigration completed successfully!")
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == '__main__':
    success = migrate_database()
    sys.exit(0 if success else 1)
