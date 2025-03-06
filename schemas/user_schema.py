from pydantic import BaseModel
from typing import Optional, Dict, Any


class UserLogin(BaseModel):
    """
    UserLogin: Schema for user login, requiring email and password.
    """

    password: str
    email: str


class UserCreate(BaseModel):
    """
    UserCreate: Schema for user registration, including optional phone number.
    """

    user_name: str
    password: str
    email: str
    avatar: str
    phone_number: Optional[str] = None


class UserResponse(BaseModel):
    """
    UserResponse: Schema for returning user details after creation or authentication.
    """

    user_name: str
    user_id: int
    email: str
    avatar: str
    phone_number: str
    meta_data: Dict[str, Any]

    class Config:
        from_attributes = True


class Refresh(BaseModel):
    """
    Refresh: Schema for handling refresh token requests.
    """

    refresh_token: str
