from fastapi import APIRouter, HTTPException, Depends
from db import get_session
from schemas import UserCreate, UserInfo
from services import UserService
import logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post('/register', response_model=UserInfo)
async def register_user(user: UserCreate, session = Depends(get_session)):
    service = UserService(session)
    try:
        user = await service.create_user(
            username=user.username,
            first_name=user.first_name,
            second_name=user.second_name,
            email=user.email,
            password=user.password
        )
        logger.info(f'Регистрация пользователя {user}')
        return user
    except ValueError as e:
        logger.info(f'Ошибка регистрации пользователя {user}')
        raise HTTPException(
            status_code=400,
            detail=f'Ошибка регистрации. \n{e}'
        )
    

