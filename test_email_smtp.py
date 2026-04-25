import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import smtplib

# Charger les variables d'environnement
load_dotenv()

# --- FIX EHLO HOSTNAME WITH COMMA ---
orig_smtp_init = smtplib.SMTP.__init__
def patched_smtp_init(self, *args, **kwargs):
    if 'local_hostname' not in kwargs or kwargs['local_hostname'] is None:
        kwargs['local_hostname'] = 'localhost'
    orig_smtp_init(self, *args, **kwargs)
smtplib.SMTP.__init__ = patched_smtp_init
# ------------------------------------

app = Flask(__name__)

# Configuration SMTP
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)

def test_send_email():
    with app.app_context():
        try:
            print(f"Tentative d'envoi d'email depuis {app.config['MAIL_USERNAME']}...")
            print(f"Serveur: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
            
            msg = Message("Test JobMatch Final Success", 
                          recipients=[app.config['MAIL_USERNAME']],
                          body="Ceci est le test final reussi pour JobMatch !")
            
            mail.send(msg)
            print("SUCCESS: Email envoye avec succes !")
        except Exception as e:
            print(f"ERREUR: {e}")

if __name__ == "__main__":
    test_send_email()
