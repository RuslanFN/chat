from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, UUID
from models import BaseModel
import uuid
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import User
class Message(BaseModel):
    __tablename__ = 'messages'
    text: Mapped[str] = mapped_column(String(2000))
    user_id: Mapped[uuid.UUID | None] = mapped_column(
                                                        UUID, 
                                                        ForeignKey('users.id', 
                                                                 ondelete='SET NULL'), 
                                                        nullable=True)
    user: Mapped['User'] = relationship(back_populates='messages')
    
