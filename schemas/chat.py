from pydantic import BaseModel, Field
from typing import List
import uuid
class PersonalChatBase(BaseModel):
    id: uuid.UUID
    user1_id: uuid.UUID
    user2_id: uuid.UUID
    chat_with: uuid.UUID
    chat_name: str

class GroupChatBase(BaseModel):
    id: uuid.UUID

class UserChasts(BaseModel):
    personal_chats: List[PersonalChatBase]
    group_chats: List[GroupChatBase]