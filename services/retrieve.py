from fastapi import HTTPException,Depends
#from pydantic import BaseModel
#from db import session
from models import Book,Author
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
#from schemas import BookSchema

class RetrieveService():
    """This is a RetrieveService class to get a book"""
    def __init__(self, session: Session) -> None:
        """
        Constructor for RetrieveService
        """
        self.session = session
       
    def hello(self):
        """
        This function performs when no endpoints are given.
        Returns:
        Literal: Returns hello
        """
        return "hello"
    
    def get_books(self):
        results=self.session.query(Book).all()
        return results
    
    def paginate_books(self,page_number : int=1,page_size: int=5):
        
        """
        This function performs when no specific endpoints are given.
        Returns:
        Returns all books in db
        """
        offset=(page_number-1)*page_size
        results = self.session.query(Book).options(joinedload(Book.author)).offset(offset).limit(page_size).all()
        return results
 
    
    def get_individual_book(self,book_id : int):
        """
        This function performs when specific endpoints are given.
        validation:
            matches the given id with db.If no match found ,then execptation rises.
        Returns:
            Returns the specific book in db
        """    
        result = self.session.query(Book).options(joinedload(Book.author)).filter(Book.id == book_id).first()
        #if not result :
        #   raise HTTPException(status_code=404, detail="Item not found")
        
        return result
    
    def get_author(self):
        results = self.session.query(Author).all()
        return results
    