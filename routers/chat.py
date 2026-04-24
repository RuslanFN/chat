from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_session
from schemas import UserChasts
from services import UserService, ChatService
from utils import verify_password, hash_password
from utils import create_access_token, decode_access_token
from .auth import get_current_user
import uuid
import logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get('/chats', response_model=UserChasts)
async def get_chats(
    request: Request,
    current_user = Depends(get_current_user),
    session = Depends(get_session)):
    service = ChatService(session)
    chats = await service.get_chats_by_user(current_user.id)
    return chats
