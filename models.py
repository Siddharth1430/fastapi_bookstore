
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type
Base = declarative_base()
class Author(Base):
    """
    Author: Represents an author with a relationship to books.
    """
    __tablename__ = 'authors' 
    author_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    no_of_books_published = Column(Integer)
    user_id = Column(Integer ,ForeignKey('users.user_id'),index= True)
    user= relationship("Users",back_populates="authors")
    books=relationship("Book", back_populates="author")

class Book(Base):
    """
    Book: Represents a book with details including title, description, edition, and publication date.
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer,ForeignKey('authors.author_id'),index=True)
    #author = Column(String)
    description = Column(String)
    edition = Column(Integer)
    #year = Column(Integer)
    published_at = Column(DateTime)
    author=relationship("Author", back_populates="books")

class Users(Base):
    """    
    Users: Represents a user with authentication-related details.
    """
    __tablename__ = 'users'
    user_id = Column(Integer,primary_key=True,index=True)
    user_name =Column(String,index=True)  
    password = Column(String)
    email = Column(String, index = True)
    avatar = Column(String)
    phone_number = Column(String)
    meta_data = Column(mutable_json_type(dbtype=JSONB, nested=True))
    authors =relationship("Author",back_populates="user")
=======
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
class Author(Base):
    """
    Author: Represents an author with a relationship to books.
    """
    __tablename__ = 'authors' 
    author_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    no_of_books_published = Column(Integer)
    books=relationship("Book", back_populates="author")

class Book(Base):
    """
    Book: Represents a book with details including title, description, edition, and publication date.
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer,ForeignKey('authors.author_id'),index=True)
    #author = Column(String)
    description = Column(String)
    edition = Column(Integer)
    #year = Column(Integer)
    published_at = Column(DateTime)
    author=relationship("Author", back_populates="books")

class Users(Base):
    """    
    Users: Represents a user with authentication-related details.
    """
    __tablename__ = 'users'
    user_id = Column(Integer,primary_key=True,index=True)
    user_name =Column(String,index=True)  
    password = Column(String)
    email = Column(String, index = True)
    avatar = Column(String)
    phone_number = Column(String)

