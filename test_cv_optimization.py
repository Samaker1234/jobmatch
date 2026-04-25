#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'optimisation du CV en fonction d'une offre d'emploi
"""

import json
from app import app

def test_cv_optimization():
    """Test l'optimisation CV pour une offre d'emploi"""
    
    # CV exemple
    cv_text = """
    Jean Dupont
    Email: jean@email.com | Tel: 06 12 34 56 78
    
    EXPERIENCE PROFESSIONNELLE
    Développeur Web - Entreprise ABC (2020-2023)
    - Développé des applications web en JavaScript
    - Travaillé sur des projets agiles
    - Participé aux code reviews
    
    COMPETENCES
    - JavaScript, HTML, CSS
    - React
    - Git
    - Agile/Scrum
    
    FORMATION
    - Licence Informatique (2019)
    """
    
    # Offre d'emploi exemple
    job_offer_text = """
    Offre d'emploi: Développeur Full Stack Senior
    
    Nous recherchons un Développeur Full Stack expérimenté pour rejoindre notre équipe.
    
    Compétences requises:
    - JavaScript/TypeScript (essentiel)
    - React ou Vue.js
    - Node.js et Express
    - PostgreSQL ou MongoDB
    - Docker et Kubernetes
    - CI/CD (Jenkins, GitLab CI)
    - AWS ou GCP
    - Expérience Agile minimale 3 ans
    - Excellente communication en français et anglais
    
    Responsabilités:
    - Concevoir et développer des architectures scalables
    - Mentoraer les développeurs juniors
    - Participer aux décisions architecturales
    - Optimiser les performances applicatives
    
    Nice to have:
    - Expérience avec Kubernetes
    - Contribution open-source
    - Certification cloud
    """
    
    print("=" * 70)
    print("TEST D'OPTIMISATION CV POUR OFFRE D'EMPLOI")
    print("=" * 70)
    
    with app.test_client() as client:
        payload = {
            'cv_text': cv_text,
            'job_offer_text': job_offer_text
        }
        
        print("\n[TEST 1] Optimisation du CV pour l'offre d'emploi")
        print("-" * 70)
        
        response = client.post('/api/optimize-cv-for-offer',
                              json=payload,
                              headers={'Content-Type': 'application/json'})
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            optimization = data.get('optimization', {})
            
            print("\n[OK] Optimisation reussie!")
            print(f"\nScore Matching: {optimization.get('score_matching', 0)}/100")
            
            print("\n📌 MOTS-CLES TROUVES:")
            keywords_found = optimization.get('keywords_found', [])
            if keywords_found:
                for kw in keywords_found[:5]:
                    print(f"  ✓ {kw}")
            
            print("\n❌ MOTS-CLES MANQUANTS:")
            keywords_missing = optimization.get('keywords_missing', [])
            if keywords_missing:
                for kw in keywords_missing[:5]:
                    print(f"  • {kw}")
            
            print("\n🎯 COMPETENCES PRESENTES:")
            comp_presentes = optimization.get('competences_presentes', [])
            if comp_presentes:
                for comp in comp_presentes[:3]:
                    print(f"  ✓ {comp}")
            
            print("\n⚠️  COMPETENCES MANQUANTES:")
            comp_manquantes = optimization.get('competences_manquantes', [])
            if comp_manquantes:
                for comp in comp_manquantes[:5]:
                    print(f"  • {comp}")
            
            print("\n💡 SUGGESTIONS D'AMELIORATION:")
            suggestions = optimization.get('suggestions', [])
            for i, sugg in enumerate(suggestions[:3], 1):
                print(f"\n  {i}. {sugg.get('section', 'N/A')} ({sugg.get('priorite', 'N/A')})")
                print(f"     Suggestion: {sugg.get('suggestion', 'N/A')}")
                print(f"     Exemple: {sugg.get('exemple', 'N/A')[:100]}...")
            
            print("\n📝 SECTIONS A AJOUTER:")
            sections = optimization.get('sections_a_ajouter', [])
            if sections:
                for section in sections[:3]:
                    print(f"  • {section}")
            
            print("\n" + "=" * 70)
            print("TEST REUSSI - L'OPTIMISATION FONCTIONNE!")
            print("=" * 70)
        else:
            data = response.get_json()
            print(f"\n[ERREUR] {data.get('error', 'Erreur inconnue')}")
            return False
    
    return True

if __name__ == '__main__':
    import sys
    try:
        success = test_cv_optimization()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERREUR CRITIQUE] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
