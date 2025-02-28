from fastapi import Depends,HTTPException,UploadFile
from models import Book,Author
from sqlalchemy.orm import Session
from db import session
from pydantic import BaseModel
from db import get_db 
from schemas import BookCreate,AuthorCreate
import cloudinary.uploader
import os
from dotenv import load_dotenv  
from fastapi.responses import StreamingResponse

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
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

    def upload_file(self,file: UploadFile,user: dict):
        """
        This function uploads the file .
        validation:
            ensures file is in the pdf format
            file doesnt exceed the limited size
        Returns:
            returns the file that is uploaded.
        """
        size=len( file.file.read())
        if size > 10*1024*1024:
            raise HTTPException(status_code=404, detail="File size exceeds the limit")
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File is not a pdf")
        file.file.seek(0)
        cloudinary.uploader.upload(file.file,resource_type="raw")
        return {"message" : "uploaded sucessfully"}

    def file_stream(self, file: UploadFile):
        def chunk():
            chunk_size =10 * 1024
            while True:
                chunk= file.read(chunk_size)
                if chunk:
                    yield chunk
        return StreamingResponse(chunk(), media_type="application/pdf")