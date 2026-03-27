from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_session
from services import UserService
from utils import verify_password, hash_password
from utils import create_access_token, decode_access_token
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer('login')
def get_current_user(
        token: OAuth2PasswordBearer,
        session = Depends(get_session)):
    service = UserService(session)
    payload = decode_access_token(token)
    if payload and 'sub' in payload:
        user_uuid = payload['sub']
        user = service.get_user(user_uuid)
        if user:
            return user
        return HTTPException(
            401,
            detail='Пользователь не найден')
    return HTTPException(
            401,
            detail='Пользователь не найден')
     
@router.post('/login')
def login(
    credentails: OAuth2PasswordRequestForm = Depends(), 
    session = Depends(get_session)):
    service = UserService(session)
    user = service.get_user_by_username(credentails.username)
    hashed_password = hash_password(credentails.password)
    if user and verify_password(hashed_password,
                                   user.hashed_password):
        return create_access_token({'sub': user.id})
    return HTTPException(
        status_code=401,
        detail= 'Неправильный логин или пароль'
        )
    
    