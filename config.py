import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cropyield-secret-2024')
    
    # Database
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    DB_NAME = os.environ.get('DB_NAME', 'crop_yield_db')
    
    # External APIs
    CEREBRAS_API_KEY = os.environ.get('CEREBRAS_API_KEY', '')
    WEATHER_API_URL = os.environ.get('WEATHER_API_URL', 'https://api.open-meteo.com/v1/forecast')
    
    # File Upload
    MAX_UPLOAD_SIZE = int(os.environ.get('MAX_UPLOAD_SIZE', 16777216))
    ALLOWED_EXTENSIONS = set(os.environ.get('ALLOWED_EXTENSIONS', 'csv,txt,json').split(','))
    
    # Security
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', 3600))
    PASSWORD_MIN_LENGTH = int(os.environ.get('PASSWORD_MIN_LENGTH', 6))
    
    # ML Models
    MODELS_DIR = 'models'
    DATA_DIR = 'data'
    
    # Supported Languages
    LANGUAGES = {
        'en': 'English',
        'kn': 'ಕನ್ನಡ',
        'hi': 'हिंदी'
    }
    
    # Crop Types
    CROPS = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 
             'Groundnut', 'Barley', 'Jowar', 'Bajra', 'Pulses', 'Vegetables']
    
    # Soil Types
    SOILS = ['Clay', 'Sandy', 'Loamy', 'Silty', 'Chalky', 'Peaty']
    
    # Seasons
    SEASONS = ['Kharif', 'Rabi', 'Zaid', 'Summer', 'Winter']
    
    # Weather Conditions
    WEATHER = ['Sunny', 'Rainy', 'Cloudy', 'Humid', 'Dry', 'Windy']
    
    # States (India)
    STATES = ['Punjab', 'Haryana', 'UP', 'MP', 'Maharashtra', 'Karnataka', 
              'Andhra Pradesh', 'Telangana', 'Gujarat', 'Rajasthan', 'Bihar', 
              'West Bengal', 'Odisha', 'Jharkhand', 'Tamil Nadu', 'Karnataka']
    
    # Recommendation Data
    NPK_RECOMMENDATIONS = {
        'Rice': {'N': '100-120', 'P': '60-80', 'K': '40-60'},
        'Wheat': {'N': '100-120', 'P': '60-80', 'K': '40-60'},
        'Maize': {'N': '120-150', 'P': '80-100', 'K': '40-60'},
        'Cotton': {'N': '80-100', 'P': '40-60', 'K': '40-60'},
        'Sugarcane': {'N': '150-200', 'P': '80-100', 'K': '80-120'},
        'Soybean': {'N': '0-20', 'P': '60-80', 'K': '40-60'},
        'Groundnut': {'N': '0-20', 'P': '80-100', 'K': '40-60'},
        'Pulses': {'N': '0-20', 'P': '60-80', 'K': '40-60'},
        'Vegetables': {'N': '100-150', 'P': '60-100', 'K': '80-120'},
    }
    
    FERTILIZER_TYPES = {
        'high_nitrogen': ['Urea', 'Ammonium Nitrate', 'Calcium Nitrate'],
        'low_nitrogen': ['Rhizobium Biofertilizer', 'Single Super Phosphate', 'Compost'],
        'high_phosphorus': ['Superphosphate', 'Phosphate Rock', 'Bone Meal'],
        'high_potassium': ['Potassium Chloride', 'Potassium Sulfate', 'Wood Ash'],
        'balanced': ['NPK 15-15-15', 'NPK 10-10-10', 'NPK 20-20-20']
    }
    
    PESTICIDE_RECOMMENDATIONS = {
        'Rice': ['Neem Oil', 'Carbofuran', 'Imidacloprid'],
        'Wheat': ['Thiamethoxam', 'Hexaconazole', 'Propiconazole'],
        'Maize': ['Endosulfan', 'Lambda-cyhalothrin', 'Chlorpyrifos'],
        'Cotton': ['Spinosad', 'Profenofos', 'Deltamethrin'],
        'Sugarcane': ['Carbofuran', 'Monocrotophos', 'Imidacloprid'],
    }
    
    IRRIGATION_SCHEDULE = {
        'Rice': {'frequency': 'Every 5-7 days', 'depth': '50mm', 'season': 'Kharif'},
        'Wheat': {'frequency': 'Every 20-25 days', 'depth': '50mm', 'season': 'Rabi'},
        'Maize': {'frequency': 'Every 10-15 days', 'depth': '50mm', 'season': 'Kharif'},
        'Cotton': {'frequency': 'Every 15-20 days', 'depth': '40mm', 'season': 'Kharif'},
        'Sugarcane': {'frequency': '8-10 times per season', 'depth': '50mm', 'season': 'Annual'},
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/crop_yield_test_db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
