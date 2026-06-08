import os
import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Optional

SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '15'))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '7'))


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def _b64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _hash_password(password: str) -> str:
    return hashlib.sha256(f'{SECRET_KEY}:{password}'.encode('utf-8')).hexdigest()


def _encode_jwt(payload: dict) -> str:
    header = {'alg': ALGORITHM, 'typ': 'JWT'}
    header_part = _b64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_part = _b64url_encode(json.dumps(payload, separators=(',', ':'), default=str).encode('utf-8'))
    signing_input = f'{header_part}.{payload_part}'.encode('ascii')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
    return f'{header_part}.{payload_part}.{_b64url_encode(signature)}'


def _decode_jwt(token: str) -> Optional[dict]:
    try:
        header_part, payload_part, signature_part = token.split('.')
        signing_input = f'{header_part}.{payload_part}'.encode('ascii')
        expected_signature = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
        actual_signature = _b64url_decode(signature_part)
        if not hmac.compare_digest(expected_signature, actual_signature):
            return None

        payload = json.loads(_b64url_decode(payload_part))
        expires_at = payload.get('exp')
        if expires_at is not None and datetime.now(timezone.utc).timestamp() > float(expires_at):
            return None
        return payload
    except (ValueError, json.JSONDecodeError, TypeError):
        return None

fake_users_db = {
    'admin': {
        'username': 'admin',
        'full_name': 'Platform Administrator',
        'email': 'admin@pharmaiq.com',
        'hashed_password': _hash_password('AdminPass123!'),
        'role': 'ADMIN'
    },
    'data_scientist': {
        'username': 'data_scientist',
        'full_name': 'Data Scientist',
        'email': 'science@pharmaiq.com',
        'hashed_password': _hash_password('DataScience123!'),
        'role': 'DATA_SCIENTIST'
    },
    'business_user': {
        'username': 'business_user',
        'full_name': 'Business User',
        'email': 'business@pharmaiq.com',
        'hashed_password': _hash_password('Business123!'),
        'role': 'BUSINESS_USER'
    }
}

refresh_token_store = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hmac.compare_digest(_hash_password(plain_password), hashed_password)


def get_user(username: str) -> Optional[dict]:
    return fake_users_db.get(username)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = get_user(username)
    if not user or not verify_password(password, user['hashed_password']):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire.timestamp()})
    return _encode_jwt(to_encode)


def create_refresh_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    user = get_user(username)
    token_data = {
        'sub': username,
        'role': user.get('role') if user else None,
        'exp': expire.timestamp(),
        'type': 'refresh'
    }
    token = _encode_jwt(token_data)
    refresh_token_store[username] = token
    return token


def decode_token(token: str) -> Optional[dict]:
    return _decode_jwt(token)


def authorize_role(token_data: dict, roles: list[str]) -> bool:
    username = token_data.get('sub')
    user = get_user(username) if username else None
    return bool(user and user.get('role') in roles)
