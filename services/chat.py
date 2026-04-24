from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import select, or_
from models import PersonalChat, GroupChat, ChatMember
from models import User
import uuid
import logging
logger = logging.getLogger(__name__)
class ChatService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_personal_chat_by_pk(self, pk: uuid.UUID) -> PersonalChat | None:
        return await self.session.get(PersonalChat, pk)
    
    async def get_personal_chat_by_users(self, user1_id: uuid.UUID, user2_id: uuid.UUID) -> PersonalChat | None:
        user1_id, user2_id = max(user1_id, user2_id), min(user1_id, user2_id)
        stmt = select(PersonalChat).where(PersonalChat.user1_id == user1_id, PersonalChat.user2_id == user2_id)
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f'Ошибка запроса к бд. \ne')
            return None
    
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
        
    async def get_chats_by_user(self, uuid: uuid.UUID):
        personal_chats = (
            select(PersonalChat).where(or_(
                PersonalChat.user1_id == uuid,
                PersonalChat.user2_id == uuid
            )).options(
                joinedload(PersonalChat.user1), 
                joinedload(PersonalChat.user2))
        )
        group_chats = select(ChatMember.group).where(ChatMember.user_id == uuid).options()

        response = {
            'personal_chats':[],
            'group_chats':[]}
        try:
            personal_chats_list = await self.session.execute(personal_chats)
            for personal_chat in personal_chats_list.scalars().all():
                if personal_chat.user1_id == uuid:
                    chat_with = personal_chat.user2_id
                    chat_name = f'{personal_chat.user2.first_name} {personal_chat.user2.second_name}'  
                else: 
                    chat_with = personal_chat.user1_id
                    chat_name = f'{personal_chat.user1.first_name} {personal_chat.user1.second_name}'
                chat_info = {
                    'chat_name': chat_name,
                    'id': personal_chat.id,
                    'user1_id': personal_chat.user1_id,
                    'user2_id': personal_chat.user2_id,
                    'chat_with': chat_with}
                response['personal_chats'].append(chat_info)
            group_chats_list = await self.session.execute(group_chats)
            response['group_chats'] = response['group_chats'] + group_chats_list.scalars().all()

        except Exception as e:
            logger.error(f'Ошибка запроса к бд. \n{e}')
        return response

