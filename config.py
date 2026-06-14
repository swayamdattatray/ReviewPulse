import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:root@localhost:3306/reviewiq_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    )
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')

    # API
    API_VERSION = os.getenv('API_VERSION', 'v1')
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api/v1')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')

    # NLP Models
    SENTIMENT_MODEL = os.getenv('SENTIMENT_MODEL', 'bert-base-uncased')
    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', 'models/pretrained')
    DEVICE = os.getenv('DEVICE', 'cpu')

    # Thresholds
    FAKE_DETECTION_THRESHOLD = float(os.getenv('FAKE_DETECTION_THRESHOLD', 0.75))
    AI_DETECTION_THRESHOLD = float(os.getenv('AI_DETECTION_THRESHOLD', 0.70))
    FEATURE_CONFIDENCE_THRESHOLD = float(os.getenv('FEATURE_CONFIDENCE_THRESHOLD', 0.5))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

    # Application Settings
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 104857600))  # 100MB
    PAGINATION_SIZE = int(os.getenv('PAGINATION_SIZE', 20))
    MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 1000))

    # Feature Flags
    ENABLE_FAKE_DETECTION = os.getenv('ENABLE_FAKE_DETECTION', 'true').lower() == 'true'
    ENABLE_AI_DETECTION = os.getenv('ENABLE_AI_DETECTION', 'true').lower() == 'true'
    ENABLE_TREND_ANALYSIS = os.getenv('ENABLE_TREND_ANALYSIS', 'true').lower() == 'true'
    ENABLE_RECOMMENDATIONS = os.getenv('ENABLE_RECOMMENDATIONS', 'true').lower() == 'true'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=300)


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }
    return config_map.get(env, DevelopmentConfig)
