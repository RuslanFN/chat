from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from models import User
import uuid
import logging
logger = logging.getLogger(__name__)
from utils import hash_password
class UserService:
    def __init__(self, session: AsyncSession        ):
        self.session = session
    async def get_user(self, id:uuid.UUID):
        return await self.session.get(User, id)
    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        try:
            user = await self.session.execute(stmt)
            return user.scalar_one_or_none()
        except MultipleResultsFound as e:
            logging.critical(f'Обнаружено несколько пользователей с одинаковым username.\n {e}')
            return None
    async def create_user(
            self,
            username: str, 
            first_name: str,
            second_name: str,
            email: str,
            password: str) -> User:
        user = User(
            username=username,
            first_name = first_name,
            second_name = second_name,
            email = email,
            hashed_password = hash_password(password)
            )
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError as e:
            await self.session.rollback()
            logging.error(e)
            raise ValueError('Данный username или email уже занят')
        except Exception as e:
            logging.error(e)
            raise ValueError('Ошибка регистрации')
            
