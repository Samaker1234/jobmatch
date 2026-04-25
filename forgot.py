from flask import Blueprint, request, jsonify
from emails import send_code_email
import random
import string
from datetime import datetime, timedelta
from models import db, ResetCode

# Création du Blueprint
forgot_bp = Blueprint('forgot', __name__)

@forgot_bp.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '').strip()
    if not email:
        return jsonify({'error': 'Email requis'}), 400

    # Vérification du format de l'email
    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({'error': 'Format d\'email invalide'}), 400

    # Vérifier si l'utilisateur existe dans la base de données
    from models import User
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Aucun compte associé à cet email'}), 404

    # Générer code 6 chiffres
    code = ''.join(random.choices(string.digits, k=6))

    # Expiration 10 min
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    try:
        # Supprimer anciens codes pour cet email
        ResetCode.query.filter_by(email=email).delete()
        db.session.commit()

        # Sauvegarder nouveau code
        reset = ResetCode(email=email, code=code, expires_at=expires_at)
        db.session.add(reset)
        db.session.commit()

        # Envoyer email
        if send_code_email(email, code):
            return jsonify({'message': 'Code envoyé par email'}), 200
        else:
            db.session.rollback()
            return jsonify({'error': 'Erreur lors de l\'envoi de l\'email'}), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@forgot_bp.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email', '').strip()
    code = data.get('code', '').strip()
    new_password = data.get('password', '').strip()

    if not all([email, code, new_password]):
        return jsonify({'error': 'Tous les champs sont requis'}), 400

    # Vérifier le code
    reset_entry = ResetCode.query.filter_by(email=email, code=code).first()
    
    if not reset_entry:
        return jsonify({'error': 'Code invalide'}), 400
    
    if reset_entry.expires_at < datetime.utcnow():
        db.session.delete(reset_entry)
        db.session.commit()
        return jsonify({'error': 'Code expiré'}), 400

    # Changer le mot de passe
    from models import User
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

    user.set_password(new_password)
    
    # Supprimer le code utilisé
    db.session.delete(reset_entry)
    db.session.commit()

    return jsonify({'message': 'Mot de passe réinitialisé avec succès'}), 200
