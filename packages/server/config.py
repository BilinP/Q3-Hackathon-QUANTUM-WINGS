import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the Flask application"""
    
    # Flask settings
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = FLASK_ENV == 'development'
    
    # Quantum TSP Solver settings
    FUEL_PRICE = float(os.environ.get('FUEL_PRICE', 0.9))
    FUEL_BURN_PER_KM = float(os.environ.get('FUEL_BURN_PER_KM', 2.5))
    DISTANCE_SCALE = int(os.environ.get('DISTANCE_SCALE', 500))
    QAOA_REPS = int(os.environ.get('QAOA_REPS', 2))
    MAX_ITER = int(os.environ.get('MAX_ITER', 150))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
