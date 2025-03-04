from pydantic import BaseModel
from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from models import Book
from datetime import datetime
from schemas.author_schemas import AuthorSchema

class BookFilter(Filter):
    """
    BookFilter: Defines filtering options for books based on title and author name.   
    """
    title: Optional[str] = None
    author_name: Optional[str] = None
    class Constants(Filter.Constants):
        model = Book

class BookSchema(BaseModel):
    """
    BookSchema: Represents the book structure with detailed attributes, including author details.
    """
    id: int
    title: str
    description: str
    edition: int
    published_at :datetime
    author_id: Optional[int] 
    author: Optional[AuthorSchema] = None
    class Config:
        from_attributes=True
        
class BookCreate(BaseModel):
    """
    BookCreate: Defines the required fields for creating a new book.
    """
    id: int
    title: str
    description: str
    edition: int
    author_id: int
    published_at :datetime
    class Config:
        from_attributes=True


