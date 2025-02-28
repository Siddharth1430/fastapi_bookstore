from sqlalchemy.orm import Session
from schemas import UserLogin,UserCreate,UserResponse,Refresh
from models import Users
from fastapi import Depends,HTTPException,status
from db import get_db
from passlib.context import CryptContext
from utils import create_access_token,create_refresh_token
from datetime import datetime, timedelta,timezone
#from fastapi_jwt_auth import AuthJWT
from jose import jwt
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    
    def __init__(self, session: Session):
        """
        Constructor for UserService
        """
        self.session = session 
 
    def refresh(self,token : Refresh):
        decoded_token= jwt.decode(token.refresh_token,SECRET_KEY , algorithms=ALGORITHM)
        time= decoded_token.get("exp")
        if datetime.utcnow().timestamp() > time:
            raise HTTPException(status_code=401, detail="Refresh token has expired.")
        access_token = create_access_token({"sub":decoded_token["sub"] }, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token}
    
    def login_user(self,user_data: UserLogin):  
        user = self.authenticate_user(user_data.email,user_data.password)
        if not user: 
            raise HTTPException(status_code=401, detail="Invalid Credentials")
        access_token = create_access_token({"sub": user_data.email}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token({"sub": user_data.email},timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

        return {"access_token": access_token, "refresh_token": refresh_token}

    def authenticate_user(self,email: str, password: str):
        user = self.get_user(email)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user
    
    def verify_password(self,plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_hashed_password(self,password: str):
        return pwd_context.hash(password)
    
    def get_user(self, email: str):
        return self.session.query(Users).filter(Users.email == email).first()
    
    def signup(self,user: UserCreate):
        db_user = self.get_user(email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="User already registered")
        hashed_password = self.get_hashed_password(user.password)
        
        user = user.model_dump()
        user["password"] = hashed_password
        new_user = Users(**user)

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user) 
        return new_user