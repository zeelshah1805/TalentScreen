import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # Model configuration
    MODEL_PATH = 'models/trained_model.pkl'
    SPACY_MODEL = 'en_core_web_sm'
    
    # Scoring thresholds
    EXCELLENT_THRESHOLD = 0.8
    GOOD_THRESHOLD = 0.6
    FAIR_THRESHOLD = 0.4