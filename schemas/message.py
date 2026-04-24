from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from .user import UserInfo
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
class MessageVueResponse(BaseModel):
    id: uuid.UUID
    text: str = Field(max_length=2000)
    updated_at: datetime = Field()
    user_id: uuid.UUID
    user: UserInfo
#class MessageVueResponse(BaseModel):
    #messages: List[MessageVue]