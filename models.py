from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=True) # Nullable for Google users
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    profession = db.Column(db.String(100))
    bio = db.Column(db.Text, nullable=True)
    achievements = db.Column(db.Text, nullable=True) # JSON or Comma separated
    skills = db.Column(db.Text, nullable=True) # JSON or Comma separated
    profile_picture = db.Column(db.String(200), nullable=True)
    banner_image = db.Column(db.String(200), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    analyses = db.relationship('CVAnalysis', backref='user', lazy=True, cascade="all, delete-orphan")
    job_profiles = db.relationship('JobProfile', backref='user', lazy=True, cascade="all, delete-orphan")
    saved_offers = db.relationship('SavedOffer', backref='user', lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade="all, delete-orphan")
    candidacies = db.relationship('Candidacy', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CVAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(200))
    final_score = db.Column(db.Float, nullable=False)
    similarity_score = db.Column(db.Float)
    coverage_score = db.Column(db.Float)
    recommendation = db.Column(db.Text)
    missing_keywords = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200))  # Comma separated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text) # JSON string
    contract_type = db.Column(db.String(50)) # CDI, CDD, Freelance
    is_generated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('job_offer.id'), nullable=False)
    status = db.Column(db.String(50), default='saved') # saved, applied, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to access offer data
    offer = db.relationship('JobOffer', backref='saved_by_users')
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default='info') # info, success, warning, match
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ResetCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(500))
    description = db.Column(db.String(200))

    @staticmethod
    def get_val(key, default=None):
        setting = SystemSetting.query.filter_by(key=key).first()
        return setting.value if setting else default

class SupportMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # ID of admin who replied
    sender_type = db.Column(db.String(20), nullable=False) # 'user' or 'admin'
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to user
    user_rel = db.relationship('User', foreign_keys=[user_id], backref='support_messages')
    admin_rel = db.relationship('User', foreign_keys=[admin_id], backref='replied_messages')

class ChatMessage(db.Model):
    """Model for storing chatbot conversation history"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Null for anonymous users
    session_id = db.Column(db.String(100), nullable=False)  # For anonymous tracking
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'bot'
    message = db.Column(db.Text, nullable=False)
    has_image = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_rel = db.relationship('User', backref='chat_messages')

class Candidacy(db.Model):
    """
    Candidature : créée automatiquement à chaque analyse ou optimisation de CV.
    L'utilisateur peut ensuite indiquer s'il a soumis le CV, gagné ou perdu.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Infos du CV/poste
    job_title = db.Column(db.String(200), nullable=False, default='Poste non défini')
    company = db.Column(db.String(100), nullable=True, default='')
    filename = db.Column(db.String(200), nullable=True)  # Nom du fichier CV
    cv_score = db.Column(db.Float, nullable=True)  # Score IA (si analysé)
    
    # Source de création
    source = db.Column(db.String(50), default='manual')  # 'analyzed', 'optimized', 'manual'
    
    # Statut de la candidature
    # submitted = a soumis le CV à une entreprise
    # won = a été embauché
    # lost = a été refusé
    # pending = pas encore soumis (statut initial)
    status = db.Column(db.String(50), default='pending')
    
    is_submitted = db.Column(db.Boolean, default=False)  # A-t-il soumis le CV ?
    feedback = db.Column(db.Text, nullable=True)  # Retour utilisateur
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime, nullable=True)  # Date de soumission
    resolved_at = db.Column(db.DateTime, nullable=True)  # Date gagné/perdu
