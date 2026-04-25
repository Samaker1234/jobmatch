#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed script pour initialiser la base de données avec des données fictives
Crée des utilisateurs de test et des exemples d'analyse
"""

import os
import sys
import json
from datetime import datetime, timedelta
import random

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models import User, CVAnalysis, JobProfile, JobOffer

def seed_users():
    """Crée des utilisateurs fictifs de test"""
    users_data = [
        {
            'firstname': 'Alice',
            'lastname': 'Dupont',
            'email': 'alice@jobmatch.test',
            'password': 'alice123',
            'profession': 'Développeuse Python'
        },
        {
            'firstname': 'Bob',
            'lastname': 'Martin',
            'email': 'bob@jobmatch.test',
            'password': 'bob123',
            'profession': 'Product Manager'
        },
        {
            'firstname': 'Charlie',
            'lastname': 'Rousseau',
            'email': 'charlie@jobmatch.test',
            'password': 'charlie123',
            'profession': 'Designer UX/UI'
        },
        {
            'firstname': 'Diana',
            'lastname': 'Garcia',
            'email': 'diana@jobmatch.test',
            'password': 'diana123',
            'profession': 'Data Scientist'
        },
        {
            'firstname': 'Docteur',
            'lastname': 'Castro',
            'email': 'castro@jobmatch.test',
            'password': 'castro123',
            'profession': 'Fondateur & Visionnaire'
        },
    ]
    
    created = 0
    for user_data in users_data:
        # Vérifier si l'utilisateur existe
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            new_user = User(
                firstname=user_data['firstname'],
                lastname=user_data['lastname'],
                email=user_data['email'],
                profession=user_data['profession']
            )
            new_user.set_password(user_data['password'])
            db.session.add(new_user)
            created += 1
            print(f"✓ Utilisateur créé : {user_data['email']}")
        else:
            print(f"✗ Utilisateur existe déjà : {user_data['email']}")
    
    db.session.commit()
    return created

def seed_cv_analyses():
    """Crée des exemples d'analyses de CV"""
    # Récupérer les utilisateurs créés
    users = User.query.all()
    
    if not users:
        print("⚠️  Aucun utilisateur trouvé. Créez d'abord les utilisateurs.")
        return 0
    
    analyses_data = [
        {
            'filename': 'CV_Alice_2024.pdf',
            'job_title': 'Développeur Python Senior - Paris',
            'final_score': 87.5,
            'similarity_score': 85.0,
            'coverage_score': 90.0,
            'recommendation': '✅ Excellent profil ! Vous possédez 90% des compétences requises.',
            'missing_keywords': json.dumps(['Kubernetes', 'GraphQL', 'Microservices'])
        },
        {
            'filename': 'CV_Bob_2024.pdf',
            'job_title': 'Product Manager - Startup Tech',
            'final_score': 72.3,
            'similarity_score': 70.0,
            'coverage_score': 74.6,
            'recommendation': '⚠️ Bon profil mais quelques lacunes. Améliorez votre connaissance du machine learning.',
            'missing_keywords': json.dumps(['Machine Learning', 'Analytics', 'A/B Testing'])
        },
        {
            'filename': 'CV_Charlie_2024.pdf',
            'job_title': 'Senior UX/UI Designer - Agence',
            'final_score': 91.2,
            'similarity_score': 92.0,
            'coverage_score': 90.4,
            'recommendation': '✅ Match exceptionnel ! Votre profil correspond parfaitement aux attentes.',
            'missing_keywords': json.dumps(['Motion Design', 'Prototyping'])
        },
    ]
    
    created = 0
    for i, analysis_data in enumerate(analyses_data):
        user = users[i % len(users)]
        
        new_analysis = CVAnalysis(
            user_id=user.id,
            filename=analysis_data['filename'],
            job_title=analysis_data['job_title'],
            final_score=analysis_data['final_score'],
            similarity_score=analysis_data['similarity_score'],
            coverage_score=analysis_data['coverage_score'],
            recommendation=analysis_data['recommendation'],
            missing_keywords=analysis_data['missing_keywords'],
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
        )
        db.session.add(new_analysis)
        created += 1
        print(f"✓ Analyse créée : {analysis_data['job_title']}")
    
    db.session.commit()
    return created

def seed_job_profiles():
    """Crée des profils d'offres d'emploi"""
    users = User.query.all()
    
    if not users:
        print("⚠️  Aucun utilisateur trouvé.")
        return 0
    
    profiles_data = [
        {
            'title': 'Développeur Python Senior',
            'company': 'TechCorp',
            'description': 'Nous recherchons un développeur Python expérimenté pour rejoindre notre équipe backend.',
            'tags': 'Python,Django,PostgreSQL,Docker'
        },
        {
            'title': 'Product Manager',
            'company': 'StartUp Innovante',
            'description': 'Pilotez nos produits digitaux et menez notre stratégie produit.',
            'tags': 'Management,Strategy,Analytics'
        },
        {
            'title': 'UX/UI Designer Senior',
            'company': 'Design Studio',
            'description': 'Créez des interfaces exceptionnelles pour nos clients premium.',
            'tags': 'Figma,Design,UX,UI'
        },
    ]
    
    created = 0
    for profile_data in profiles_data:
        for user in users[:2]:  # Assigner à quelques utilisateurs
            new_profile = JobProfile(
                user_id=user.id,
                title=profile_data['title'],
                company=profile_data['company'],
                description=profile_data['description'],
                tags=profile_data['tags']
            )
            db.session.add(new_profile)
            created += 1
    
    db.session.commit()
    print(f"✓ {created} profils de postes créés")
    return created

def clear_database():
    """Nettoie la base de données (optionnel)"""
    print("\n🗑️  Nettoyage de la base de données...")
    
    # Supprimer dans l'ordre pour respecter les contraintes FK
    CVAnalysis.query.delete()
    JobProfile.query.delete()
    JobOffer.query.delete()
    User.query.delete()
    
    db.session.commit()
    print("✓ Base de données nettoyée")

def main():
    """Fonction principale"""
    with app.app_context():
        print("\n" + "="*60)
        print("🌱 Initialisation de la base de données JobMatch")
        print("="*60 + "\n")
        
        # Optionnel : Nettoyer d'abord
        # Décommentez la ligne ci-dessous si vous voulez recommencer de zéro
        # clear_database()
        
        print("📝 Création des utilisateurs de test...")
        users_created = seed_users()
        print(f"✓ {users_created} utilisateur(s) créé(s)\n")
        
        print("📊 Création des analyses de CV...")
        analyses_created = seed_cv_analyses()
        print(f"✓ {analyses_created} analyse(s) créée(s)\n")
        
        print("💼 Création des profils de postes...")
        profiles_created = seed_job_profiles()
        print(f"\n✓ {profiles_created} profil(s) créé(s)\n")
        
        print("="*60)
        print("✨ Données fictives initialisées avec succès !")
        print("="*60)
        print("\n📋 Comptes de test disponibles :\n")
        
        users = User.query.all()
        for user in users:
            email = user.email
            password = email.split('@')[0] + '123'  # Convention de notre seed
            print(f"   Email    : {email}")
            print(f"   Password : {password}")
            print(f"   Rôle     : {user.profession}\n")

if __name__ == '__main__':
    main()
