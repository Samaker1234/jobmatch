#!/usr/bin/env python3
"""
Test des pages À Propos et Équipe
"""

from app import app

def test_pages():
    """Test l'accès aux pages"""
    with app.test_client() as client:
        print("=" * 70)
        print("TEST DES PAGES À PROPOS ET ÉQUIPE")
        print("=" * 70)
        
        # Test page À Propos
        print("\n[TEST 1] Page À Propos")
        response = client.get('/about')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[OK] Page À Propos se charge correctement")
            assert "À Propos de JobMatch" in response.data.decode('utf-8')
            assert "Notre Mission" in response.data.decode('utf-8')
            assert "Notre Vision" in response.data.decode('utf-8')
            print("[OK] Contenu attendu trouvé")
        else:
            print(f"[ERREUR] Status: {response.status_code}")
            return False
        
        # Test page Équipe
        print("\n[TEST 2] Page Présentation Équipe")
        response = client.get('/team')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[OK] Page Présentation Équipe se charge correctement")
            assert "Rencontrez Notre Équipe" in response.data.decode('utf-8')
            assert "Leadership" in response.data.decode('utf-8')
            assert "Engineering" in response.data.decode('utf-8')
            print("[OK] Contenu attendu trouvé")
        else:
            print(f"[ERREUR] Status: {response.status_code}")
            return False
        
        print("\n" + "=" * 70)
        print("TOUS LES TESTS PASSES!")
        print("=" * 70)
        print("\n✓ Les pages sont accessibles")
        print("✓ Les contenus sont chargés correctement")
        print("\nAccès direct:")
        print("  - http://localhost:5000/about")
        print("  - http://localhost:5000/team")
        
        return True

if __name__ == '__main__':
    import sys
    try:
        success = test_pages()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERREUR CRITIQUE] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
