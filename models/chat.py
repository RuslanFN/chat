from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, UUID, UniqueConstraint
from models import BaseModel
import uuid
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from models import User, Message

class PersonalChat(BaseModel):
    __tablename__ = 'personal_chats'    
    user1_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID,
        ForeignKey(
            'users.id',
            ondelete='SET NULL'
        ),
        nullable=True)
    user2_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID,
        ForeignKey(
            'users.id',
            ondelete='SET NULL'
        ),
        nullable=True)
    messages: Mapped[List['Message']] = relationship(back_populates='personal_chat')
    user1: Mapped['User'] =  relationship(foreign_keys=[user1_id],
                                           back_populates='chat_as_first')
    user2: Mapped['User'] =  relationship(foreign_keys=[user2_id], 
                                          back_populates='chat_as_second')

    __table_args__ = (
        UniqueConstraint(
            'user1_id', 'user2_id', 
            name='uix_user1_user2'),
    )

class GroupChat(BaseModel):
    __tablename__ = 'group_chats'
    messages: Mapped[List['Message']] = relationship(back_populates='group_chat')
    members: Mapped[List['ChatMember']] = relationship(secondary='chat_members', back_populates='groups')
    
class ChatMember(BaseModel):
    __tablename__ = 'chat_members'
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey(
            'users.id',
            ondelete='SET NULL')
    )
    group_chat_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey(
            'group_chats.id',
            ondelete='CASCADE'
        )
    )
    user: Mapped['User'] = relationship(back_populates='groups')
    group: Mapped['GroupChat'] = relationship(back_populates='members')
    __table_args__ =(
        UniqueConstraint(
            'user_id', 'group_chat_id',
            name='uix_user_group'
        ),

    )

