from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, UUID, CheckConstraint
from models import BaseModel
import uuid
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import User, PersonalChat, GroupChat
class Message(BaseModel):
    __tablename__ = 'messages'
    text: Mapped[str] = mapped_column(String(2000))
    personal_chat_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID,
        ForeignKey(
            'personal_chats.id',
            ondelete='CASCADE'
        ),
        nullable=True
    )
    group_chat_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID,
        ForeignKey(
            'group_chats.id',
            ondelete='CASCADE'
        ),
        nullable=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID, 
        ForeignKey(
            'users.id', 
            ondelete='SET NULL'
        ), 
        nullable=True
    )
    user: Mapped['User'] = relationship(back_populates='messages')
    personal_chat: Mapped['PersonalChat'] = relationship(back_populates='messages')
    group_chat: Mapped['GroupChat'] = relationship(back_populates='messages')

    __table_args__ = (
        CheckConstraint(
            '(personal_chat_id is NULL) != (group_chat_id is NULL)',
            name='check_message_has_only_one_type'
        ),
    )