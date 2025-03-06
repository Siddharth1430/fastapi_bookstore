from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Security, Depends
from sqlalchemy.orm import Session
from jose import jwt
from dotenv import load_dotenv
import os
from db import get_db
from models import Users

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """_summary_
    Retrieves the current authenticated user from the provided JWT token.
    Args:
        credentials (HTTPAuthorizationCredentials, optional): _description_. Defaults to Security(security).
    Raises:
        HTTPException: If the token is invalid or the user is not authenticated.
    Returns:
        dict: The decoded token payload if valid.
    """
    token = credentials.credentials
    payload = verify_jwt_token(token)
    if payload is None:
        print("payload is empty")
        raise HTTPException(status_code=403, detail="User Invalid.")
    print(payload)
    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()

    return user


def verify_jwt_token(token: str):
    """_summary_
    Verifies the JWT token
    Args:
        token (str): The JWT token to be verified.
    Returns:
        dict or None: The decoded token payload if valid, otherwise None
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token)
        return decoded_token
    except Exception as e:

        print(SECRET_KEY)
        print(token)
        print(ALGORITHM)
        print("Exception occurs while verifying token")
        print(e)
