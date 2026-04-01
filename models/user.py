from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from models import BaseModel
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from models import Message, PersonalChat, GroupChat
class User(BaseModel):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(20), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String())
    messages: Mapped[List['Message']] = relationship(back_populates='user')
    chat_as_first: Mapped[List['PersonalChat']] = relationship(back_populates='user1')
    chat_as_second: Mapped[List['PersonalChat']] = relationship(back_populates='user2')
    groups: Mapped[List['GroupChat']] = relationship(
        secondary='chat_member',
        back_populates='members') 
    @property
    def personal_chats(self):
        return self.chat_as_first + self.chat_as_second