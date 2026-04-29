from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from .user import UserInfo
from .chat import PersonalChatBase
import uuid
class PersonMessageSend(BaseModel):
    text: str = Field(max_length=2000)
    to_username:str = Field(max_length=20)

class PersonMessageSendByChatPk(BaseModel):
    text: str = Field(max_length=2000)
    chat_id: uuid.UUID
class MessageResponse(BaseModel):
    text: str = Field(max_length=2000)
    to_username:str = Field(max_length=20)
    updated_at: datetime = Field()
    chat: PersonalChatBase
    model_config = {'from_attributes': True}
class MessageVueResponse(BaseModel):
    id: uuid.UUID
    text: str = Field(max_length=2000)
    updated_at: datetime = Field()
    user_id: uuid.UUID
    user: UserInfo
    model_config = {'from_attributes': True}
#class MessageVueResponse(BaseModel):
    #messages: List[MessageVue]