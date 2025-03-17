from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class User(BaseModel):
    user_id: str
    username: str
    display_name: str
    password_hash: str
    created_at: datetime
    last_login: Optional[datetime]
    is_active: bool
    conversations: List[str]
