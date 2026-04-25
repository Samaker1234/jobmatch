import sqlite3
import os

def migrate():
    # Path to the database
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'instance', 'jobmatch.db')
    
    if not os.path.exists(db_path):
        print(f"Base de données introuvable à : {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Ajout des colonnes reset_code et reset_expiration à la table user...")
        
        # Add reset_code
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN reset_code TEXT")
            print("- Colonne reset_code ajoutée.")
        except sqlite3.OperationalError:
            print("- Colonne reset_code existe déjà.")
            
        # Add reset_expiration
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN reset_expiration DATETIME")
            print("- Colonne reset_expiration ajoutée.")
        except sqlite3.OperationalError:
            print("- Colonne reset_expiration existe déjà.")
            
        conn.commit()
        conn.close()
        print("Migration terminée avec succès.")
        
    except Exception as e:
        print(f"Erreur lors de la migration : {e}")

if __name__ == "__main__":
    migrate()
