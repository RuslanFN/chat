from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from models import BaseModel
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from models import Message, PersonalChat, GroupChat, ChatMember
class User(BaseModel):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String())
    messages: Mapped[List['Message']] = relationship(back_populates='user')
    # Для персональных чатов (пользователь-пользователь) 
    # необходимо создать две ссылки, так как 
    # пользователь может быть записан как первый и как второй 
    # в таблице персонального чата 
    chat_as_first: Mapped[List['PersonalChat']] = relationship(
        'PersonalChat',
        foreign_keys='[PersonalChat.user1_id]', # указывает на поле, которые ссылается на юзера
        back_populates='user1')
    chat_as_second: Mapped[List['PersonalChat']] = relationship(
        'PersonalChat',
        foreign_keys='[PersonalChat.user2_id]', # указывает на поле, которые ссылается на юзера
        back_populates='user2')
    memberships: Mapped[List['ChatMember']] = relationship(
        'ChatMember',
        foreign_keys='[ChatMember.user_id]', # указывает на поле, которые ссылается на юзера
        back_populates='user') 
    # Получаем все персональные чаты
    @property
    def personal_chats(self):
        return self.chat_as_first + self.chat_as_second