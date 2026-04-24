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
    # Оба realtion для модели User, 
    # поэтому мы должны уточник конкретные foreign keys
    user1: Mapped['User'] =  relationship(foreign_keys=[user1_id], 
                                           back_populates='chat_as_first')
    user2: Mapped['User'] =  relationship(foreign_keys=[user2_id], 
                                          back_populates='chat_as_second')
    # Необходимо, чтобы между двумя любыми 
    # пользователями существовал только один чат
    __table_args__ = (
        UniqueConstraint(
            'user1_id', 'user2_id', 
            name='uix_user1_user2'),
    )

class GroupChat(BaseModel):
    __tablename__ = 'group_chats'
    messages: Mapped[List['Message']] = relationship(back_populates='group_chat')
    members: Mapped[List['ChatMember']] = relationship(back_populates='group')

# Класс ассоцияция для пользователя и группового чата. 
# Ссылается на User и GroupChat и имеет к ним relation 
class ChatMember(BaseModel):
    __tablename__ = 'chat_members'
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey(
            'users.id',
            ondelete='SET NULL') # Обычно в мессенджерах оставляют 
    )
    group_chat_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey(
            'group_chats.id',
            ondelete='CASCADE'
        )
    )
    user: Mapped['User'] = relationship(back_populates='memberships')
    group: Mapped['GroupChat'] = relationship(back_populates='members')
    # Каждая запись участника группы должна быть 
    # уникальна по полям user_id и group_chat_id
    __table_args__ =(
        UniqueConstraint(
            'user_id', 'group_chat_id',
            name='uix_user_group'
        ),

    )

