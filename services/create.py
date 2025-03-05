from fastapi import Depends,HTTPException
from models import Book,Author
from sqlalchemy.orm import Session
from schemas.book_schemas import BookCreate
from schemas.author_schemas import AuthorCreate

class CreateService:
    """This is a CreateService class to create a book"""
    def __init__(self,session: Session) -> None:
        """
        Constructor for CreateService
        """
        self.session = session 
        
    def create_book(self,book: BookCreate,user: dict):
        """
        This function creates the new book .
        validation:
            ensures no two books can have same title
        Returns:
            returns the book that is created.
        """
        results = self.session.query(Book).filter(Book.title== book.title).first()
        if results:
            raise HTTPException(status_code=404, detail="Book already exist")
    
        new= Book(**book.model_dump()) 
    
        self.session.add(new)
        self.session.commit()
        self.session.refresh(new)
        return new

    def create_author(self, book_id: int,author: AuthorCreate,user: dict):
        """
        This function creates the new author .
        validation:
            ensures no two authors can have same name
        Returns:
            returns the author that is created.
        """
        book =self.session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        results = self.session.query(Author).filter(Author.author_id == author.author_id).first()
        if  results:
            return results
        new_author = Author(**author.model_dump())
        self.session.add(new_author)
        self.session.commit()
        self.session.refresh(new_author)            
        book.author_id=new_author.author_id
        self.session.commit()     
        return new_author

    