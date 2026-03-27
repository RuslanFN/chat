from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from models import User
import uuid
import logging

class UserService:
    def __init__(self, session: Session):
        self.session = session
    def get_user(self, id:uuid.UUID):
        return self.session.get(User, id)
    def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        try:
            user = self.session.execute(stmt).scalar_one_or_none()
            return user
        except MultipleResultsFound as e:
            logging.critical(f'Обнаружено несколько пользователей с одинаковым username.\n {e}')
            return None
    