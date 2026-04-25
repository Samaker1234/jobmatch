#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crée la base SQLite `jobmatch.db` et les tables définies dans `models.py`.
Exécuter depuis le dossier `flask_app`:

    python create_db.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        print(f"Configuration SQLALCHEMY_DATABASE_URI: {db_uri}")
        print('Création des tables (si non-existantes)...')
        db.create_all()
        if db_uri and db_uri.startswith('sqlite:///'):
            path = db_uri.replace('sqlite:///', '')
            print(f"Fichier SQLite créé / utilisé: {os.path.abspath(path)}")
        print('✓ Opération terminée')
