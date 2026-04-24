from fastapi import Depends, HTTPException, status, APIRouter, Response, Request, WebSocket, WebSocketException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_session
from services import UserService
from utils import verify_password, hash_password
from utils import create_access_token, decode_access_token
import uuid
import logging
logger = logging.getLogger(__name__)
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer('login', auto_error=False)
async def get_token_from_cookie_or_header(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            return auth_header.replace('Bearer ', '')
    return token

async def get_current_user_ws(websocket: WebSocket):
    token = websocket.cookies.get('access_token')
    logger.info('Получаю токен с куков для web_socket')
    if not token:
        token = websocket.headers.get('access_token')
        logger.info('В куках токена нет. Получаю токен с заголовков для web_socket')
    try:
        payload = decode_access_token(token)
        payload['sub']
    except Exception as e:
        logger.exception(f'Ошибка websocket соединения {e}')
        raise WebSocketException(
            status_code=401,
            )


async def get_current_user(
        request: Request,
        token: str|None = Depends(oauth2_scheme),
        session = Depends(get_session)):
    if not token:
        logger.info('Токена нет, смотрю в куки')
        token = request.cookies.get('access_token')
    if not token:
        logger.info('Токена нет, смотрю в заголовках')
        auth_header = request.headers.get('Authorization')
        if auth_header:
            return auth_header.replace('Bearer ', '')
    service = UserService(session)
    payload = decode_access_token(token)
    if payload and 'sub' in payload:
        user_uuid = uuid.UUID(payload['sub'])
        user = await service.get_user(user_uuid)
        logger.info(user)
        if user:
            return user
        raise HTTPException(
            401,
            detail='Пользователь не найден')
    raise HTTPException(
            401,
            detail='Ошибка аутентификации')
     
@router.post('/login')
async def login(
    response: Response,
    credentails: OAuth2PasswordRequestForm = Depends(), 
    session = Depends(get_session)):
    service = UserService(session)
    user = await service.get_user_by_username(credentails.username)
    print(credentails.username)
    print(user)
    if user and verify_password(credentails.password,
                                   user.hashed_password):
        logger.info(f'Пользователь {user.username} авторизован')
        user_token = create_access_token({'sub': str(user.id)})
        response.set_cookie(
            key='access_token',
            value=user_token['access_token'],
            secure=False,
            httponly=True,
            samesite="lax",
            max_age=18000   
        )
        return {'message': 'Успешный вход'}
    raise HTTPException(
        status_code=401,
        detail= 'Неправильный логин или пароль'
        )
    
    