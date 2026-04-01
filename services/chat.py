from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models import PersonalChat
from models import PersonalChat
import uuid
import logging
logger = logging.getLogger(__name__)
class ChatService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_personal_chat_by_pk(self, pk: uuid.UUID) -> PersonalChat | None:
        return await self.session.get(PersonalChat, pk)

    async def create_personal_chat(self, user1_id, user2_id) -> PersonalChat | None:
        user1_id, user2_id = max(user1_id, user2_id), min(user1_id, user2_id)
        personal_chat = PersonalChat(
            user1_id=user1_id,
            user2_id=user2_id            
        )
        self.session.add(personal_chat)
        try:
            await self.session.commit()
            await self.session.refresh(personal_chat)
            return personal_chat
        except IntegrityError as e:
            logger.error(f'Ошибка создания чата. \n{e}')
            await self.session.rollback()
            return None

    async def delete_personal_chat(self, personal_chat: PersonalChat) -> None:
        await self.session.delete(personal_chat)
        await self.session.commit()
        
