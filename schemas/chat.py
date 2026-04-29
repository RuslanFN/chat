from pydantic import BaseModel, Field
from typing import List
from .user import UserInfo
import uuid
class PersonalChatBase(BaseModel):
    id: uuid.UUID
    user1: UserInfo
    user2: UserInfo
    chat_with: uuid.UUID
    chat_name: str
    model_config = {'from_attributes': True}

class GroupChatBase(BaseModel):
    id: uuid.UUID

class UserChasts(BaseModel):
    personal_chats: List[PersonalChatBase]
    group_chats: List[GroupChatBase]