from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy.sql import func

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    
    author_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    no_of_books_published = Column(Integer)
    books=relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer,ForeignKey('authors.author_id'),index=True)
    #author = Column(String)
    description = Column(String)
    edition = Column(Integer)
    #year = Column(Integer)
    #created_at = Column(DateTime, server_default=func.now())
    author=relationship("Author", back_populates="books")

class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer,primary_key=True,index=True)
    user_name =Column(String,index=True)  
    password = Column(String)
    email = Column(String, index = True)
    avatar = Column(String)