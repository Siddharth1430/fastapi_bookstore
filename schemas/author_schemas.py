from pydantic import BaseModel
from typing import Optional

class AuthorSchema(BaseModel):
    """
    AuthorSchema: Represents the structure of an author with optional ID.    
    """
    author_id:Optional[int] = None
    name: str
    no_of_books_published: int    
    class Config:
        from_attributes =True
        
class AuthorCreate(BaseModel):
    """
    AuthorCreate: Defines the required fields for creating a new author.
    """
    author_id : int
    name: str
    no_of_books_published: int
