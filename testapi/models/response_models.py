from pydantic import BaseModel
from typing import Optional
from datetime import datetime

"""
Module for Pydantic models for API response data
"""
class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: Optional[datetime]

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

class UserResponse(BaseModel):
    user_id: str
    username: str
    display_name: Optional[str]
    created_at: datetime
