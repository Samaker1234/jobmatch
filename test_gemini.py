import sys
import os
import google.generativeai as genai

# Ajouter le dossier courant au path
sys.path.append(os.getcwd())

from gemini_service import gemini_service
from config import Config

def test_gemini():
    print(f"--- DEBUG ACTIVATION GEMINI ---")
    
    # Configurer API key pour le list_models direct
    genai.configure(api_key=Config.GEMINI_API_KEY)
    
    print("Liste des modèles disponibles:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Erreur lors du listage des modèles: {e}")

    print(f"\nService Gemini réellement activé: {gemini_service.enabled}")
    
    if gemini_service.enabled:
        print(f"Modèle actuel: {gemini_service.model.model_name}")
        print("Envoi d'un message test...")
        try:
            # On tente un message très simple
            response = gemini_service.model.generate_content("Réponds uniquement 'OK'")
            print(f"Réponse AI: {response.text}")
        except Exception as e:
            print(f"Erreur lors de l'appel AI: {e}")
    else:
        print("Le service Gemini est désactivé.")
    print(f"------------------------------")

if __name__ == "__main__":
    test_gemini()
