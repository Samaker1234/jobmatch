import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Utilisation de l'URL de la base de données
db_url = os.environ.get('DATABASE_URL')
# Nettoyage de l'URL si nécessaire (enlever pgbouncer=true pour psycopg2)
if '?' in db_url:
    db_url = db_url.split('?')[0]

try:
    print("Connexion à Supabase...")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    print("Modification de la colonne password_hash...")
    # Requête SQL pour augmenter la taille de la colonne
    cur.execute('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(255);')
    
    conn.commit()
    print("Succès ! La colonne a été agrandie à 255 caractères.")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Erreur lors de la modification : {e}")
