from pydantic import BaseModel
from typing import List,Optional

class AuthorSchema(BaseModel):
    author_id:Optional[int] = None
    name: str
    no_of_books_published: int
    
    class Config:
        from_attributes =True
        
class AuthorCreate(BaseModel):
    #id: Optional[int]=None
    author_id : int
    name: str
    no_of_books_published: int


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    edition: int
    author_id: Optional[int] 
    author: Optional[AuthorSchema] = None
    class Config:
        from_attributes=True
        
class BookCreate(BaseModel):
    id: int
    title: str
    description: str
    edition: int
    author_id: int
    
    class Config:
        from_attributes=True


class UserLogin(BaseModel):
    
    password : str
    email : str
        

class UserCreate(BaseModel):
    user_name: str
    password: str
    email : str
    avatar : str
    
class UserResponse(BaseModel):
    user_name: str
    user_id: int
    email : str
    avatar : str
    class Config:
        from_attributes = True
        
class Refresh(BaseModel):
    refresh_token : str
    
    
