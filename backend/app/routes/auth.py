from fastapi import APIRouter, HTTPException, status
from app.schemas import UserCreate, UserOut, LoginRequest

router = APIRouter()

@router.post('/register', response_model=UserOut)
def register(user: UserCreate):
    # Placeholder registration logic
    if user.username == 'existing':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')
    return {
        'id': 1,
        'username': user.username,
        'email': user.email,
        'is_active': True
    }

@router.post('/login')
def login(request: LoginRequest):
    # Placeholder login logic
    if request.username != 'admin' or request.password != 'password':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    return {'access_token': 'demo-token', 'token_type': 'bearer'}
