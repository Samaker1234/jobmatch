"""
Script de migration pour ajouter la colonne google_id à la table user (SQLite).

À exécuter depuis le dossier `flask_app` :

    python migrate_google_id.py

Ce script est idempotent : si la colonne existe déjà, il ne fait rien.
"""

import os
import sqlite3


def get_db_path() -> str:
    """Retourne le chemin du fichier SQLite utilisé par l'application."""
    # Chemin par défaut utilisé par Flask pour `sqlite:///jobmatch.db`
    base_dir = os.path.dirname(__file__)
    instance_dir = os.path.join(base_dir, "instance")
    default_path = os.path.join(instance_dir, "jobmatch.db")

    if os.path.exists(default_path):
        return default_path

    # Fallback : chercher n'importe quel .db dans instance/
    if os.path.isdir(instance_dir):
        for name in os.listdir(instance_dir):
            if name.endswith(".db"):
                return os.path.join(instance_dir, name)

    # Dernier recours : jobmatch.db à la racine du projet
    root_fallback = os.path.join(base_dir, "jobmatch.db")
    return root_fallback


def migrate_google_id():
    db_path = get_db_path()
    print(f"Utilisation de la base de données : {os.path.abspath(db_path)}")

    if not os.path.exists(db_path):
        print("❌ Fichier de base de données introuvable. Lance d'abord `python create_db.py`.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Récupérer les colonnes existantes
        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Colonnes actuelles de `user` : {columns}")

        if "google_id" in columns:
            print("La colonne `google_id` existe déjà, aucune action nécessaire.")
            conn.close()
            return

        print("Ajout de la colonne `google_id` à la table user...")
        cursor.execute("ALTER TABLE user ADD COLUMN google_id VARCHAR(100)")
        conn.commit()
        print("Colonne `google_id` ajoutée avec succès.")

        conn.close()
    except sqlite3.Error as e:
        print(f"Erreur SQLite pendant la migration : {e}")
    except Exception as e:
        print(f"Erreur inattendue pendant la migration : {e}")


if __name__ == "__main__":
    migrate_google_id()

