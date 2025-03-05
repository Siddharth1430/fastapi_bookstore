from fastapi_filter import FilterDepends
from models import Book,Author,Users
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from schemas.book_schemas import BookFilter

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
        """_summary_
        to diaplay all books
        Returns:
            list of book schema.
        """
        results= self.session.query(Book).all()
        return results
    
    def get_users(self):
        """_summary_
        to diaplay all users
        Returns:
            list of user schema.
        """
        results= self.session.query(Users).all()
        return results
    
    def get_author(self):
        """_summary_
        get all authors
        Returns:
            List of authors
        """
        results = self.session.query(Author).all()
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
        return result
    
    
    def get_filtered_books(self, book: BookFilter = FilterDepends(BookFilter)):
        """_summary_
        To display books by appying filter based on query
        Args:
            book (BookFilter, optional): _description_. Defaults to FilterDepends(BookFilter).
        Returns:
            List of Book schema
        """
        result =self.session.query(Book).options(joinedload(Book.author))
        if book.author_name:
            result =result.join(Author).filter(Author.name == book.author_name)
        if book.title:
            result =result.filter(Book.title == book.title)
        result = result.order_by(Book.published_at.desc()).all()
        return result
    

