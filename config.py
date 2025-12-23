"""
Configuration settings for Multi-Object Tracking Dashboard
"""

import os

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'outputs'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'jpg', 'jpeg', 'png'}
    
    # Model settings
    DEFAULT_MODEL = os.environ.get('YOLO_MODEL', 'yolov8n.pt')
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONF_THRESHOLD', '0.25'))
    
    # Tracking settings
    MAX_AGE = int(os.environ.get('TRACK_MAX_AGE', '30'))
    MIN_HITS = int(os.environ.get('TRACK_MIN_HITS', '3'))
    IOU_THRESHOLD = float(os.environ.get('TRACK_IOU_THRESHOLD', '0.3'))
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', '5000'))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Add production-specific settings here


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
