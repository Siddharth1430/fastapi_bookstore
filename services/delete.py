from fastapi import Depends,HTTPException
from models import Book,Author
from sqlalchemy.orm import Session
from db import session
from db import get_db 

class DeleteService:
    """This is a DeleteService class to delete a book"""
    def __init__(self, session: Session) -> None:
        """
        Constructor for DeleteService
        """
        self.session = session

    def delete_book(self,book_id : int):
        """
        This function which gets the id of he book which needs to be deleted.
        Returns:
        Dict: return a dic to display a message
        """

        results = self.session.query(Book).filter(Book.id == book_id).first()
        if not results :
            raise HTTPException(status_code=404, detail="Item not found")
        self.session.delete(results)
        self.session.commit()
        return {"message":"book deleted"}
    
    def delete_author(self, author_id : int):
        """
        This function which gets the id of he author which needs to be deleted.
        Returns:
        Dict: return a dic to display a message
        """
        results = self.session.query(Author).filter(Author.author_id == author_id).first()
        if not results :
            raise HTTPException(status_code=404, detail="Author not found")
        
        book_count = self.session.query(Book).filter(Book.author_id == author_id).count()
        if book_count > 0:
           raise HTTPException(status_code=409, detail="Cannot delete author having books")
        
        self.session.delete(results)
        self.session.commit()
        return {"message":"author deleted"}




