#!/usr/bin/env python
"""
Migration script to add profile_picture and banner_image columns to the user table.
This script handles databases that don't have these columns yet.
"""
import sqlite3
import os
import sys

def migrate_database():
    """Add missing columns to user table if they don't exist"""
    
    # Default database path for SQLite (adjust if different)
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'jobmatch.db')
    
    # Try alternative paths
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), 'instance', 'jobmaths.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        print("Checking for alternative database locations...")
        instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
        if os.path.exists(instance_dir):
            db_files = [f for f in os.listdir(instance_dir) if f.endswith('.db')]
            if db_files:
                db_path = os.path.join(instance_dir, db_files[0])
                print(f"Found database: {db_path}")
            else:
                print("No database files found in instance directory")
                return False
        else:
            print("Instance directory not found")
            return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if profile_picture column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'profile_picture' in columns and 'banner_image' in columns:
            print("✓ Columns 'profile_picture' and 'banner_image' already exist in user table")
            conn.close()
            return True
        
        # Add missing columns
        if 'profile_picture' not in columns:
            print("Adding 'profile_picture' column...")
            cursor.execute("ALTER TABLE user ADD COLUMN profile_picture VARCHAR(200)")
            print("✓ Added profile_picture column")
        
        if 'banner_image' not in columns:
            print("Adding 'banner_image' column...")
            cursor.execute("ALTER TABLE user ADD COLUMN banner_image VARCHAR(200)")
            print("✓ Added banner_image column")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    success = migrate_database()
    sys.exit(0 if success else 1)
