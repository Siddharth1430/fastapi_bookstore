from sqlalchemy.orm import Session
from schemas.user_schema import UserLogin,UserCreate,Refresh
from models import Users
from fastapi import Depends,HTTPException
from passlib.context import CryptContext
from utils import create_access_token,create_refresh_token
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
counter =1

class UserService:
    
    def __init__(self, session: Session):
        """
        Constructor for UserService
        """
        self.session = session 
 
    def refresh(self,token : Refresh):
        """
        Generates a new access token using a valid refresh token.
        Args:
            token (Refresh): The refresh token provided by the user.
        Raises:
            HTTPException: If the refresh token has expired.
        Returns:
            dict: A dictionary containing the new access token.
        """
        decoded_token= jwt.decode(token.refresh_token,SECRET_KEY , algorithms=ALGORITHM)
        time= decoded_token.get("exp")
        if datetime.utcnow().timestamp() > time:
            raise HTTPException(status_code=401, detail="Refresh token has expired.")
        access_token = create_access_token({"sub":decoded_token["sub"] }, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token}
    
    def login_user(self,user_data: UserLogin):  
        """
        Authenticates a user and generates access and refresh tokens.
        Args:
            user_data (UserLogin): The login credentials.
        Raises:
            HTTPException: If authentication fails due to invalid credentials.
        Returns:
            dict: A dictionary containing the access token and refresh token.
        """
        user = self.authenticate_user(user_data.email,user_data.password)
        if not user: 
            raise HTTPException(status_code=401, detail="Invalid Credentials")
        access_token = create_access_token({"sub": user_data.email}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token({"sub": user_data.email},timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        return {"access_token": access_token, "refresh_token": refresh_token}

    def authenticate_user(self,email: str, password: str):
        """_summary_
        To authenticate the user 
        Args:
            email (str): email of user
            password (str): password of user
        Returns:
            Literal : True if authenticated else False
        """
        user = self.get_user(email)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user
    
    def verify_password(self,plain_password, hashed_password):
        """_summary_
        To verify the given password 
        Args:
            plain_password (_type_):normal password entered by user
            hashed_password (bool): hassed passwor stored in the db
        Returns:
            _type_:True for valid or else False
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_hashed_password(self,password: str):
        """_summary_
        To get hashed password
        Args:
            password (str):entered by user
        Returns:
            str : hashed password
        """
        return pwd_context.hash(password)
    
    def get_user(self, email: str):
        """_summary_
        To get current user
        Args:
            email (str): email of user
        Returns:
            Return the user schema
        """
        return self.session.query(Users).filter(Users.email == email).first()
    
    def signup(self,user: UserCreate):
        """_summary_
        To signup or register a new user
        Args:
            user (UserCreate): the yuser schema that has info about user.
        Raises:
            HTTPException: rises if User already exist.
        Returns:
            return new user schema
        """
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
    
    
