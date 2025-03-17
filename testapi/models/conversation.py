from pydantic import BaseModel
from datetime import datetime
from typing import List
from .message import Message

class Conversation(BaseModel):
    conversation_id: str
    user_id: str
    title: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
