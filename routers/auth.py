from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_session
from services import UserService
from utils import verify_password, hash_password
from utils import create_access_token, decode_access_token
import logging
logger = logging.getLogger(__name__)
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer('login')
async def get_current_user(
        token: OAuth2PasswordBearer,
        session = Depends(get_session)):
    service = UserService(session)
    payload = decode_access_token(token)
    if payload and 'sub' in payload:
        user_uuid = payload['sub']
        user = await service.get_user(user_uuid)
        if user:
            return user
        raise HTTPException(
            401,
            detail='Пользователь не найден')
    raise HTTPException(
            401,
            detail='Пользователь не найден')
     
@router.post('/login')
async def login(
    credentails: OAuth2PasswordRequestForm = Depends(), 
    session = Depends(get_session)):
    service = UserService(session)
    user = await service.get_user_by_username(credentails.username)
    if user and verify_password(credentails.password,
                                   user.hashed_password):
        logger.info(f'Пользователь {user.username} авторизован')
        return create_access_token({'sub': str(user.id)})
    logger.info(f'Неудачная попытка входа для {user.username}')
    raise HTTPException(
        status_code=401,
        detail= 'Неправильный логин или пароль'
        )
    
    