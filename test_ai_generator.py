"""
Tests pour le générateur d'offres d'emploi par IA
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ai_job_generator import JobOfferAIGenerator
import json

def test_basic_generation():
    """Test: Génération basique d'une offre"""
    print("🧪 Test 1: Génération basique")
    generator = JobOfferAIGenerator()
    offer = generator.generate_offer()
    
    assert offer['id'].startswith('JOB_'), "ID invalide"
    assert offer['title'], "Titre manquant"
    assert offer['company'], "Entreprise manquante"
    assert len(offer['required_skills']) > 0, "Pas de compétences"
    assert offer['generated'] == True, "Flag 'generated' incorrect"
    
    print(f"  ✓ Offre générée: {offer['title']} @ {offer['company']}")
    return True

def test_batch_generation():
    """Test: Génération d'un lot"""
    print("🧪 Test 2: Génération en batch")
    generator = JobOfferAIGenerator()
    offers = generator.generate_batch(count=5)
    
    assert len(offers) == 5, f"Nombre d'offres incorrect: {len(offers)}"
    assert all(offer['generated'] for offer in offers), "Certaines offres non marquées comme générées"
    
    print(f"  ✓ Lot de {len(offers)} offres générées")
    return True

def test_role_type_filtering():
    """Test: Filtrage par type de rôle"""
    print("🧪 Test 3: Filtrage par type de rôle")
    generator = JobOfferAIGenerator()
    
    for role_type in ['development', 'design', 'management', 'data', 'qa']:
        offer = generator.generate_offer(role_type=role_type)
        assert offer['department'], f"Département manquant pour {role_type}"
        print(f"  ✓ {role_type}: {offer['title']}")
    
    return True

def test_custom_criteria():
    """Test: Génération avec critères personnalisés"""
    print("🧪 Test 4: Génération avec critères")
    generator = JobOfferAIGenerator()
    
    custom_skills = ['Python', 'Docker', 'PostgreSQL', 'FastAPI']
    offer = generator.generate_by_requirements(
        required_skills=custom_skills,
        experience_level='Senior',
        location='Paris'
    )
    
    assert all(skill in offer['required_skills'] or skill in offer['nice_to_have_skills'] 
               for skill in custom_skills[:2]), "Compétences non incluses"
    assert offer['experience_level'] == 'Senior', "Niveau d'expérience incorrect"
    assert offer['location'] == 'Paris', "Localisation incorrecte"
    
    print(f"  ✓ Offre personnalisée créée")
    print(f"    - Compétences: {', '.join(custom_skills)}")
    print(f"    - Niveau: {offer['experience_level']}")
    print(f"    - Lieu: {offer['location']}")
    return True

def test_offer_structure():
    """Test: Vérifier la structure de l'offre"""
    print("🧪 Test 5: Structure de l'offre")
    generator = JobOfferAIGenerator()
    offer = generator.generate_offer()
    
    required_fields = [
        'id', 'title', 'company', 'location', 'contract_type',
        'experience_level', 'salary_min', 'salary_max', 'description',
        'required_skills', 'nice_to_have_skills', 'responsibilities',
        'benefits', 'posted_date', 'application_deadline', 'department',
        'team_size', 'remote_percentage', 'generated'
    ]
    
    missing_fields = [field for field in required_fields if field not in offer]
    assert not missing_fields, f"Champs manquants: {missing_fields}"
    
    print(f"  ✓ Tous les {len(required_fields)} champs présents")
    return True

def test_data_consistency():
    """Test: Cohérence des données"""
    print("🧪 Test 6: Cohérence des données")
    generator = JobOfferAIGenerator()
    offer = generator.generate_offer()
    
    # Vérifier les salaires
    assert offer['salary_min'] < offer['salary_max'], "Salaires incohérents"
    assert offer['salary_min'] >= 30000, "Salaire min trop bas"
    assert offer['salary_max'] <= 150000, "Salaire max trop haut"
    
    # Vérifier les dates
    from datetime import datetime
    posted = datetime.strptime(offer['posted_date'], '%d/%m/%Y')
    deadline = datetime.strptime(offer['application_deadline'], '%d/%m/%Y')
    assert deadline > posted, "Deadline avant la date de publication"
    
    # Vérifier les listes
    assert len(offer['required_skills']) <= 10, "Trop de skills requis"
    assert len(offer['responsibilities']) <= 10, "Trop de responsabilités"
    
    print(f"  ✓ Données cohérentes")
    print(f"    - Salaire: {offer['salary_min']/1000:.0f}k - {offer['salary_max']/1000:.0f}k €")
    print(f"    - Deadline valide: {deadline.strftime('%d/%m/%Y')}")
    return True

def test_offer_serialization():
    """Test: Sérialisation JSON"""
    print("🧪 Test 7: Sérialisation JSON")
    generator = JobOfferAIGenerator()
    offers = generator.generate_batch(3)
    
    try:
        json_str = json.dumps(offers)
        parsed = json.loads(json_str)
        assert len(parsed) == 3, "Désérialisation échouée"
        print(f"  ✓ {len(offers)} offres sérialisées en JSON")
    except Exception as e:
        print(f"  ✗ Erreur de sérialisation: {e}")
        return False
    
    return True

def test_performance():
    """Test: Performance"""
    print("🧪 Test 8: Performance")
    import time
    
    generator = JobOfferAIGenerator()
    
    # Test génération simple
    start = time.time()
    generator.generate_offer()
    simple_time = time.time() - start
    
    # Test batch
    start = time.time()
    generator.generate_batch(10)
    batch_time = time.time() - start
    
    print(f"  ✓ Génération simple: {simple_time*1000:.2f}ms")
    print(f"  ✓ Batch de 10: {batch_time*1000:.2f}ms ({batch_time/10*1000:.2f}ms/offre)")
    
    assert simple_time < 0.5, "Génération trop lente"
    assert batch_time < 5, "Batch trop lent"
    
    return True

def run_all_tests():
    """Exécuter tous les tests"""
    print("\n" + "="*60)
    print("🚀 TESTS DU GÉNÉRATEUR D'OFFRES IA")
    print("="*60 + "\n")
    
    tests = [
        test_basic_generation,
        test_batch_generation,
        test_role_type_filtering,
        test_custom_criteria,
        test_offer_structure,
        test_data_consistency,
        test_offer_serialization,
        test_performance,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            print(f"  ✗ Erreur: {e}\n")
            results.append((test.__name__, False))
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s)")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
