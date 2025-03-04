from datetime import datetime, timedelta,timezone
from jose import  jwt
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generates a new access token using JWT.

    Args:
        data (Dict): The payload data to encode in the token.
        expires_delta (timedelta, optional): Expiration time for the token. 
        Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: A JWT access token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta:  Optional[timedelta] = None):
    """
    Generates a new refresh token using JWT.

    Args:
        data (Dict): The payload data to encode in the token.
        expires_delta (timedelta, optional): Expiration time for the token. 
            Defaults to REFRESH_TOKEN_EXPIRE_DAYS.

    Returns:
        str: A JWT refresh token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


