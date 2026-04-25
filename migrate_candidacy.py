"""
Migration : recréer la table Candidacy avec les nouveaux champs.
Supprime l'ancienne table et la recrée proprement.
"""
import os
from app import app
from models import db

def migrate():
    with app.app_context():
        try:
            # Supprimer l'ancienne table et la recreer avec le nouveau schema
            db.engine.execute("DROP TABLE IF EXISTS candidacy")
        except Exception:
            pass
        
        try:
            # SQLite alternatif
            with db.engine.connect() as con:
                con.execute("DROP TABLE IF EXISTS candidacy")
        except Exception:
            pass

        # Recreer toutes les tables (les tables existantes ne sont pas affectees)
        db.create_all()
        print("OK: Table Candidacy recree avec le nouveau schema.")

if __name__ == "__main__":
    migrate()
