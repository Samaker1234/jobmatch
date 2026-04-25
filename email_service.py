import resend
import os
from dotenv import load_dotenv

# Charger le .env (utile si lancé indépendamment pour test)
load_dotenv()

# Initialisation Resend avec la clé API du .env
resend.api_key = os.getenv("RESEND_API_KEY")

def send_reset_code_email(email_destinataire, code):
    """
    Envoie un email avec le code de réinitialisation
    """
    try:
        # Note: 'from' doit être un domaine vérifié sur Resend.
        sender = "JobMatch <samakedelamou858@gmail.com>"
        
        response = resend.Emails.send({
            "from": sender,
            "to": email_destinataire,
            "subject": "Code de réinitialisation JobMatch",
            "html": f"""
            <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
                <h2 style="color: #333;">Bonjour,</h2>
                <p style="font-size: 16px; color: #555;">Votre code de réinitialisation (valable 10 minutes) est :</p>
                <div style="background-color: #f4f4f4; padding: 15px; text-align: center; border-radius: 5px; margin: 20px 0;">
                    <strong style="font-size: 32px; letter-spacing: 5px; color: #2d3436;">{code}</strong>
                </div>
                <p style="font-size: 14px; color: #888;">Si vous n'avez pas demandé ce code, ignorez cet email.</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #aaa; text-align: center;">À bientôt sur JobMatch !<br>Envoyé via Resend</p>
            </div>
            """
        })
        print("Email envoyé avec succès :", response)
        return True
    except Exception as e:
        print("Erreur Resend détaillée :", str(e))
        return False

if __name__ == "__main__":
    # Test rapide si le fichier est exécuté directement
    test_email = os.getenv("TEST_EMAIL") # Vous pouvez ajouter TEST_EMAIL dans votre .env
    if test_email:
        print(f"Envoi d'un test à {test_email}...")
        send_reset_code_email(test_email, "123456")
    else:
        print("Définissez TEST_EMAIL dans votre .env pour tester ce fichier.")
