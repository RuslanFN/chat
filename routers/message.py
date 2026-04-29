from fastapi import APIRouter, HTTPException, Depends, Query
from db import get_session
from services import MessageService, UserService, ChatService
from schemas import PersonMessageSend, PersonMessageSendByChatPk, MessageResponse, MessageVueResponse
from schemas import PersonalChatBase
from .auth import get_current_user
from .ws import manager
from typing import List
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post('/send_message', response_model=MessageResponse)
async def send_message(
    data: PersonMessageSend, 
    current_user=Depends(get_current_user), 
    session=Depends(get_session)
    ):
    message_service = MessageService(session)
    user_service = UserService(session)
    chat_service = ChatService(session)
    current_user_id = current_user.id
    try:
        recipent_user = await user_service.get_user_by_username(data.to_username)
        recipent_user_id = recipent_user.id
        chat = await chat_service.get_personal_chat_by_users(current_user_id, recipent_user_id)
        if not chat:
            chat = await chat_service.create_personal_chat(current_user_id, recipent_user_id)
        message = await message_service.create_message(
            data.text, 
            current_user_id, 
            personal_chat_id=chat['id'],
            )
        chat_json = PersonalChatBase.model_validate(chat).model_dump(mode='json')
        return {
            'text':  data.text,
            'to_username': data.to_username,
            'updated_at': message.updated_at,
            'chat': chat_json
        }
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail='Ошибка отправки собщения'
        )

@router.post('/send_message_to_chat', response_model=MessageVueResponse)
async def send_message_to_chat(
    data: PersonMessageSendByChatPk, 
    current_user=Depends(get_current_user), 
    session=Depends(get_session)
    ):
    message_service = MessageService(session)
    chat_service = ChatService(session)
    current_user_id = current_user.id
    try:
        chat = await chat_service.get_personal_chat_by_pk(data.chat_id)
        if chat.user1_id != current_user_id and chat.user2_id != current_user_id:
            raise HTTPException(
                status_code=401,
                detail='Вы не имеете доступа к этому чату'
            )
        
        message = await message_service.create_message(
            data.text, 
            current_user.id, 
            personal_chat_id=chat.id)
        message_json = MessageVueResponse.model_validate(message).model_dump(mode='json')
        await manager.broadcast_by_chat(message_json, chat.id)
        return message
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail='Ошибка отправки собщения'
        )

@router.get('/messages')
async def get_messegas(
    current_user=Depends(get_current_user), 
    session=Depends(get_session)
    ):
    service = MessageService(session)
    logger.info(current_user.id)
    messages =  await service.get_last_messages(current_user.id)
    logger.info(messages)
    return messages

@router.get('/messages/{chat_id}', response_model=List[MessageVueResponse])
async def get_messages_by_chat(
    chat_id: uuid.UUID, 
    current_user=Depends(get_current_user), 
    session=Depends(get_session)
    ):
    service = MessageService(session)
    try:
        return await service.get_last_messages_by_chat_id(
            chat_id=chat_id, 
            current_user=current_user.id
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail='Вы не имеете доступа к сообщениям в этом чате'            
        )