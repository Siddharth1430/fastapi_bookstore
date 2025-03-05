from fastapi import Depends, HTTPException
from models import Book
from sqlalchemy.orm import Session
from schemas.book_schemas import BookPublish


class PatchServices:
    def __init__(self, session: Session):
        self.session = session

    def publish_book(self, book: BookPublish):
        result = self.session.query(Book).filter(Book.title == book.title).first()
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")

        result.is_published = True  # type:ignore
        self.session.commit()
        return {"Message": "Book is published"}
