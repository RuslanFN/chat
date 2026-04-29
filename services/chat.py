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
        return await self.session.get(
            PersonalChat, 
            pk, 
            options=(joinedload(PersonalChat.user1),
                      joinedload(PersonalChat.user2))
        )
    
    async def get_personal_chat_by_users(self, current_user_id: uuid.UUID, recipent_user_id: uuid.UUID) -> PersonalChat | None:
        user1_id, user2_id = max(current_user_id, recipent_user_id), min(current_user_id, recipent_user_id)
        stmt = (select(PersonalChat)
                .where(
                    PersonalChat.user1_id == user1_id, 
                    PersonalChat.user2_id == user2_id)
                .options(
                    joinedload(PersonalChat.user1), 
                    joinedload(PersonalChat.user2))
                )
        try:
            result = await self.session.execute(stmt)
            new_personal_chat = result.scalar_one_or_none()
            if new_personal_chat.user1_id == current_user_id:
                    chat_with = new_personal_chat.user2_id
                    chat_name = f'{new_personal_chat.user2.first_name} {new_personal_chat.user2.second_name}'  
            else: 
                chat_with = new_personal_chat.user1_id
                chat_name = f'{new_personal_chat.user1.first_name} {new_personal_chat.user1.second_name}'
            chat_info = {
                'chat_name': chat_name,
                'id': new_personal_chat.id,
                'user1': new_personal_chat.user1,
                'user2': new_personal_chat.user2,
                'chat_with': chat_with}
            return chat_info
        except Exception as e:
            logger.error(f'Ошибка запроса к бд. \ne')
            return None
    
    async def create_personal_chat(self, current_user_id: uuid.UUID, recipent_user_id: uuid.UUID) -> PersonalChat | None:
        user1_id, user2_id = max(current_user_id, recipent_user_id), min(current_user_id, recipent_user_id)
        personal_chat = PersonalChat(
            user1_id=user1_id,
            user2_id=user2_id            
        )
        self.session.add(personal_chat)
        try:
            await self.session.commit()
            new_personal_chat =  (await self.session.get(
                PersonalChat, 
                personal_chat.id, 
                options=(
                    joinedload(PersonalChat.user1),
                    joinedload(PersonalChat.user2))
                )
            )
            if new_personal_chat.user1_id == current_user_id:
                    chat_with = personal_chat.user2_id
                    chat_name = f'{personal_chat.user2.first_name} {personal_chat.user2.second_name}'  
            else: 
                chat_with = personal_chat.user1_id
                chat_name = f'{personal_chat.user1.first_name} {personal_chat.user1.second_name}'
            chat_info = {
                'chat_name': chat_name,
                'id': personal_chat.id,
                'user1': personal_chat.user1,
                'user2': personal_chat.user2,
                'chat_with': chat_with}
            return chat_info
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
                    'user1': personal_chat.user1,
                    'user2': personal_chat.user2,
                    'chat_with': chat_with}
                response['personal_chats'].append(chat_info)
            group_chats_list = await self.session.execute(group_chats)
            response['group_chats'] = response['group_chats'] + group_chats_list.scalars().all()

        except Exception as e:
            logger.error(f'Ошибка запроса к бд. \n{e}')
        return response

