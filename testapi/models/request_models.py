from pydantic import BaseModel
from typing import Optional
from services.validation_service import ValidationService

class SendMessageRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

class UserCreateRequest(BaseModel):
    username: str
    password: str
    display_name: Optional[str] = None

    model_config = ValidationService.get_model_config()
    validate_username = ValidationService.validate_username
    validate_password = ValidationService.validate_password

class LoginRequest(BaseModel):
    username: str
    password: str
