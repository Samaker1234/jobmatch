from flask_mail import Message
from flask import current_app
import os
import logging

logger = logging.getLogger(__name__)


def send_code_email(to_email: str, code: str):
    """
    Envoie un email avec le code de réinitialisation via Flask-Mail (SMTP)
    """
    from app import mail  # Import local pour éviter les imports circulaires
    
    try:
        subject = "Code de réinitialisation JobMatch"
        sender = current_app.config.get('MAIL_DEFAULT_SENDER')
        
        msg = Message(subject, recipients=[to_email], sender=sender)
        
        msg.html = f"""
        <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 40px; background-color: #ffffff; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; border-radius: 12px; font-weight: 800; font-size: 24px; letter-spacing: 1px;">
                    JobMatch
                </div>
            </div>
            <h2 style="color: #1e293b; margin-top: 0; font-weight: 700;">Bonjour,</h2>
            <p style="color: #475569; font-size: 16px; line-height: 1.6;">Vous avez demandé la réinitialisation de votre mot de passe. Voici votre code de sécurité unique :</p>
            <div style="background: #f8fafc; border: 2px dashed #e2e8f0; padding: 30px; text-align: center; border-radius: 16px; margin: 30px 0;">
                <h1 style="font-size: 42px; color: #6366f1; letter-spacing: 10px; margin: 0; font-family: monospace; font-weight: 800;">
                    {code}
                </h1>
                <p style="color: #94a3b8; font-size: 12px; margin-top: 15px; margin-bottom: 0;">Ce code expirera dans 10 minutes.</p>
            </div>
            <p style="color: #475569; font-size: 16px; line-height: 1.6;">Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email en toute sécurité. Votre mot de passe restera inchangé.</p>
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #f1f5f9; text-align: center;">
                <p style="color: #6366f1; font-weight: 600; font-size: 14px; margin-bottom: 5px;">L'équipe JobMatch</p>
                <small style="color: #94a3b8;">Transformez votre carrière avec l'IA</small>
            </div>
        </div>
        """
        
        mail.send(msg)
        logger.info("Email de code de réinitialisation envoyé à %s", to_email)
        return True
    except Exception as e:
        logger.error("Erreur lors de l'envoi via Flask-Mail pour %s : %s", to_email, e, exc_info=True)
        return False

def send_cv_email(to_email: str, pdf_buffer, filename: str):
    """
    Envoie le CV optimisé en pièce jointe PDF
    """
    from app import mail

    try:
        subject = "Votre CV optimisé par JobMatch IA"
        sender = current_app.config.get('MAIL_DEFAULT_SENDER')

        msg = Message(subject, recipients=[to_email], sender=sender)

        msg.html = f"""
        <div style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 40px; background-color: #ffffff; border-radius: 16px; border: 1px solid #f0f0f0;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; border-radius: 12px; font-weight: 800; font-size: 24px;">
                    JobMatch
                </div>
            </div>
            <h2 style="color: #1e293b; font-weight: 700;">Bonjour,</h2>
            <p style="color: #475569; font-size: 16px; line-height: 1.6;">Bonne nouvelle ! Notre IA a terminé l'optimisation de votre CV pour maximiser vos chances de succès.</p>
            <p style="color: #475569; font-size: 16px; line-height: 1.6;">Vous trouverez votre <b>CV amélioré au format PDF</b> en pièce jointe de cet email.</p>
            
            <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin: 25px 0; border-left: 4px solid #6366f1;">
                <p style="margin: 0; color: #1e293b; font-weight: 600;">Ce qui a été amélioré :</p>
                <ul style="color: #475569; font-size: 14px; margin-top: 10px;">
                    <li>Mise en page professionnelle</li>
                    <li>Utilisation de verbes d'action</li>
                    <li>Optimisation des mots-clés techniques</li>
                    <li>Structure optimisée pour les ATS</li>
                </ul>
            </div>

            <p style="color: #475569; font-size: 16px; line-height: 1.6;">Bonne chance dans vos recherches !</p>
            
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #f1f5f9; text-align: center;">
                <p style="color: #6366f1; font-weight: 600; font-size: 14px; margin-bottom: 5px;">L'équipe JobMatch</p>
                <small style="color: #94a3b8;">Votre partenaire carrière intelligent</small>
            </div>
        </div>
        """
        
        # Attacher le PDF
        msg.attach(filename, "application/pdf", pdf_buffer.read())

        mail.send(msg)
        logger.info("Email avec CV optimisé envoyé à %s (fichier: %s)", to_email, filename)
        return True
    except Exception as e:
        logger.error("Erreur d'envoi du CV par mail à %s : %s", to_email, e, exc_info=True)
        return False
