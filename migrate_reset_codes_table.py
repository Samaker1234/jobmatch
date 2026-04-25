import sqlite3
import os

def migrate():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'instance', 'jobmatch.db')
    
    if not os.path.exists(db_path):
        print(f"Base de données introuvable à : {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Création de la table reset_code...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reset_code (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                code TEXT NOT NULL,
                expires_at DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("Table reset_code créée avec succès.")
        
    except Exception as e:
        print(f"Erreur lors de la migration : {e}")

if __name__ == "__main__":
    migrate()
