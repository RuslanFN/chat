from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models import PersonalChat
from models import Message
from models import User
from models import GroupChat
import uuid
import logging
logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self, session):
        self.session = session
    
    async def get_message(self, pk: uuid.UUID) -> Message:
        return await self.session.get(Message, pk) 
    
    async def create_message(self, 
        text: str, 
        user_id: uuid.UUID, 
        personal_chat_id: uuid.UUID | None,
        group_chat_id: uuid.UUID | None) -> Message | None:
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
            await self.session.refresh(message)
            return message
        except Exception as e:
            logger.error(f'Ошибка при создании сообщения. {e}')
            await self.session.rollback()
            return None
    
    async def delete_message(self, message: Message) -> None:
        await self.session.delete(message)
        await self.session.commit()
        logger.info('Сообщение удалено')




        