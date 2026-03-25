from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from models import BaseModel
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from models import Message 
class User(BaseModel):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(20))
    first_name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(50))
    messages: Mapped[List['Message']] = relationship(back_populates='user')
    