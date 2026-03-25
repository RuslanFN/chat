from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from models import BaseModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import User
class Message(BaseModel):
    __tablename__ = 'messages'
    text: Mapped[str] = mapped_column(String(2000))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    user: Mapped['User'] = relationship(back_populates='messages')
    
