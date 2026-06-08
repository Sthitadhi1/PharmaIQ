import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./backend.db')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
MODEL_PATH = os.getenv('MODEL_PATH', 'ml_engine/saved_models/')
API_VERSION = os.getenv('API_VERSION', 'v1')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
