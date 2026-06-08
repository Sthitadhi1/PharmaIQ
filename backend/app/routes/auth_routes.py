from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.utils.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    authorize_role,
    get_user
)
from app.utils.rate_limiter import RateLimiter

router = APIRouter(prefix='/api/auth', tags=['Authentication'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')
limiter = RateLimiter(limit=10, window_seconds=60)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload or payload.get('type') != 'access':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication token')
    user = get_user(payload.get('sub'))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


@router.post('/token', response_model=TokenResponse)
def login(request: LoginRequest):
    client_key = f'auth:{request.username}'
    if not limiter.allow(client_key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail='Too many login attempts')
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token({'sub': user['username'], 'role': user['role'], 'type': 'access'}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(user['username'])
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'role': user['role']
    }


@router.post('/refresh')
def refresh_token(request: RefreshRequest):
    payload = decode_token(request.refresh_token)
    if not payload or payload.get('type') != 'refresh':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    username = payload.get('sub')
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token payload')
    access_token = create_access_token({'sub': username, 'role': payload.get('role'), 'type': 'access'}, expires_delta=timedelta(minutes=15))
    return {'access_token': access_token, 'refresh_token': request.refresh_token, 'token_type': 'bearer', 'role': payload.get('role')}


@router.get('/me')
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {'username': current_user['username'], 'role': current_user['role'], 'email': current_user['email']}
