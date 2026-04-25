#!/usr/bin/env python3
import json
from app import app

with app.test_client() as client:
    payload = {
        'message': 'Bonjour, comment peux-tu m\'aider avec ma carrière?',
        'history': []
    }
    response = client.post('/api/chat', 
                          json=payload,
                          headers={'Content-Type': 'application/json'})
    print(f"Status: {response.status_code}")
    data = response.get_json()
    if response.status_code == 200:
        print("[OK] Reponse recue:")
        print(data.get('response', 'Aucune reponse')[:500])
    else:
        print(f"[ERREUR] {data}")
