import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Repository root (…/PharmaIQ). Relative paths below are resolved against it so the
# API behaves the same whether it is started from the repo root or from backend/.
REPO_ROOT = Path(__file__).resolve().parents[3]


def _resolve(path_value: str) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else REPO_ROOT / path


DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./backend.db')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
MODEL_PATH = str(_resolve(os.getenv('MODEL_PATH', 'ml_engine/saved_models/')))
DATA_DIR = _resolve(os.getenv('DATA_DIR', '.'))
UPLOAD_DIR = _resolve(os.getenv('UPLOAD_DIR', 'backend/documents'))
API_VERSION = os.getenv('API_VERSION', 'v1')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
    if origin.strip() and origin.strip() != '*'
]
MAX_UPLOAD_BYTES = int(os.getenv('MAX_UPLOAD_BYTES', str(10 * 1024 * 1024)))
ALLOWED_UPLOAD_EXTENSIONS = {'.pdf', '.txt', '.csv'}
