import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def debug_smtp():
    # Correction : utiliser .env pour les valeurs
    host = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    port = int(os.environ.get('MAIL_PORT', 587))
    user = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')
    
    print(f"Debug SMTP vers {host}:{port} avec local_hostname='localhost'")
    print(f"User: {user}, Pwd length: {len(password) if password else 0}")
    
    try:
        server = smtplib.SMTP(host, port, local_hostname='localhost')
        server.set_debuglevel(1)
        server.starttls()
        print("TLS start successful")
        server.login(user, password)
        print("Login successful")
        server.quit()
        print("SUCCESS!")
    except Exception as e:
        print(f"ERREUR: {e}")

if __name__ == "__main__":
    debug_smtp()
