"""
Configuration de l'application Flask JobMatch
"""

import os

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    
    # NLP Settings
    MIN_KEYWORD_LENGTH = 3
    MAX_KEYWORDS_DISPLAY = 20
    MIN_JOB_TEXT_LENGTH = 50
    
    # Scoring
    HIGH_SCORE_THRESHOLD = 70
    MEDIUM_SCORE_THRESHOLD = 50
    
    SIMILARITY_WEIGHT = 0.6
    COVERAGE_WEIGHT = 0.4
    
    # NLTK
    NLTK_STOPWORDS_LANGUAGE = 'french'
    
    # TF-IDF
    TFIDF_MAX_FEATURES = 500
    TFIDF_NGRAM_RANGE = (2, 3)
    
    # Gemini API Configuration
    # Chargez la clé depuis les variables d'environnement uniquement.
    # Ne pas laisser de valeur par défaut en dur dans le dépôt.
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-pro')
    GEMINI_ENABLED = os.environ.get('GEMINI_ENABLED', '1') == '1'
    
    # Database (Fallback to SQLite if no Supabase URL provided)
    _db_url = os.environ.get('SQLALCHEMY_DATABASE_URI', os.environ.get('DATABASE_URL', 'sqlite:///jobmatch.db'))
    if _db_url and _db_url.startswith('postgresql'):
        # SQLAlchemy requires 'postgresql://' instead of 'postgres://' (common in Heroku/Render)
        if _db_url.startswith('postgres://'):
            _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
        # Fix for pgbouncer error: remove ?pgbouncer=true if present
        if '?' in _db_url:
            _db_url = _db_url.split('?')[0]
            
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # Google OAuth2
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    # Optionnel: URL de redirection explicite (sinon, générée avec url_for)
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')


class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Configuration de test"""
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'test_uploads')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
