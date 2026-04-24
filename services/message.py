from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload
from models import PersonalChat
from models import Message
from models import User
from models import GroupChat, ChatMember
import uuid
import logging
from typing import List
from .user import UserService
from .chat import ChatService
logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_message(self, pk: uuid.UUID) -> Message:
        return await self.session.get(Message, pk) 
    
    async def create_message(self, 
        text: str, 
        user_id: uuid.UUID, 
        personal_chat_id: uuid.UUID | None = None,
        group_chat_id: uuid.UUID | None = None) -> Message | None:
        '''
        Create message for group or personal chat.
        You need to give only one argument of "personal_chat" 
        and "group_chat" arguments. 
        You can't give both arguments
        '''
        if personal_chat_id is None == group_chat_id is None:
            logger.error('Неправильно передан id чата. Сообщение не создано')
            raise ValueError('Неправильно переданы данные чата. Необходимо передать один из двух параметров "personal_chat" или "group_chat"') 
        message = Message(
            text = text,
            user_id = user_id,
            personal_chat_id = personal_chat_id,
            group_chat_id = group_chat_id
        )
        self.session.add(message)
        try:
            await self.session.commit()
            logger.info(f'Сообщение создано. id: {message.id}')
            stmt = (select(Message)
                    .where(Message.id == message.id)
                    .options(joinedload(Message.user)))
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except Exception as e:
            logger.error(f'Ошибка при создании сообщения. {e}')
            await self.session.rollback()
            return None
    
    async def delete_message(self, message: Message) -> None:
        await self.session.delete(message)
        await self.session.commit()
        logger.info('Сообщение удалено')        

    async def get_last_messages(self,
                                current_uuid: uuid.UUID, 
                                count = 20):
        user_chats_ids = select(PersonalChat.id).where(or_(
            PersonalChat.user1_id == current_uuid,
            PersonalChat.user2_id == current_uuid),
        ).union_all(
            select(ChatMember.group_chat_id).where(
                ChatMember.user_id == current_uuid
            )
        )
        
        stmt = select(Message).where(
            or_(
                Message.personal_chat_id.in_(
                    user_chats_ids
                ),
                Message.group_chat_id.in_(
                    user_chats_ids
                )
            ) 
        ).order_by(Message.created_at.desc()).limit(count)
        messages = await self.session.execute(stmt)
        return messages.scalars().all()


    async def get_last_messages_by_chat_id(self, 
                                           chat_id: uuid.UUID,
                                           current_user: uuid.UUID):
        chat = await self.session.get(PersonalChat, chat_id)
        if chat:
            if chat.user1_id != current_user and chat.user2_id != current_user:
                raise PermissionError('У данного пользователя нет доступа к сообщениям этого чата')
        else:     
            chat = await self.session.get(GroupChat. chat_id)
            stmt = select(ChatMember).where(
                ChatMember.user_id == current_user,
                ChatMember.group_chat_id == chat_id
            )
            if chat and not (await self.session.execute(stmt)).one_or_none():
                raise PermissionError('У данного пользователя нет доступа к сообщениям этого чата')
        stmt = select(Message).where(
            or_(
                Message.personal_chat_id == chat_id,
                Message.group_chat_id == chat_id
            )
        ).options(
            joinedload(Message.user)
        ).order_by(
            Message.created_at.desc()
        ).limit(50)
        try:
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f'Ошибка загрузки сообщений {e}')
            return []