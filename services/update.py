from fastapi import Depends,HTTPException
from models import Book,Author,Users
from sqlalchemy.orm import Session
from schemas.author_schemas import AuthorCreate
from schemas.book_schemas import BookCreate
from schemas.user_schema import UserCreate

class UpdateService:
    """This is a UpdateService class to update a book"""
    def __init__(self, session: Session) -> None:
        """
        Constructor for UpdateService
        """
        self.session = session 
          
    def update_book(self,book_id: int, book: BookCreate,user: dict):
        """
        This function updates the book by getting the id from user to locate the book.
        validation:
            matches the given id with db.If no match found ,then execptation rises.
            if user try to update the title to the existing one then exceptation rises
        Returns:
        returns the updated book
        """
        results = self.session.query(Book).filter(Book.id == book_id).first()
        if not results :
            raise HTTPException(status_code=404, detail="Item not found")
        existing_book = self.session.query(Book).filter(Book.title== book.title).first()
        if existing_book :
            if existing_book.id != results.id:
                raise HTTPException(status_code=409, detail="Book already exist with same title")
        
        results.title = book.title
        #results.author = book.author
        results.description = book.description
        results.edition = book.edition
        self.session.commit()
        self.session.refresh(results)
        return results
    
    def update_author(self, author_id: int, author:AuthorCreate,user: dict):
        """
        This function updates the author by getting the id from user to locate the author.
        validation:
            matches the given id with db.If no match found ,then execptation rises.
            if user try to update the name to the existing one then exceptation rises
        Returns:
        returns the updated author
        """
        results = self.session.query(Author).filter(Author.author_id == author_id).first()
        if not results :
            raise HTTPException(status_code=404, detail="Author not found")
    
        results.name = author.name
        results.no_of_books_published = author.no_of_books_published
        
        self.session.commit()
        return results
    
    def update_user(self,user_id : int, users: UserCreate, user : dict):
        """_summary_
        To update the credentials or info about user.
        Args:
            user_id (int): _description_
            users (UserCreate): _description_
            user (dict): _description_
        Raises:
            HTTPException: If user credential not match
        Returns:
            A user schema
        """
        results = self.session.query(Users).filter(Users.user_id==user_id).first()
        if not results:
           raise HTTPException(status_code=404, detail="User not found")
        results.user_name= users.user_name
        results.password = users.password
        results.email = users.email
        results.avatar = users.avatar
        results.phone_number = users.phone_number
        
        self.session.commit()
        return results
