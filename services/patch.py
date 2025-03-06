from fastapi import Depends, HTTPException
from models import Book, Users, Author
from sqlalchemy.orm import Session, joinedload
from schemas.book_schemas import BookPublish


class PatchServices:
    def __init__(self, session: Session):
        self.session = session

    def publish_book(self, book: BookPublish, user: Users):
        result = (
            self.session.query(Book)
            # .options(joinedload(Book.author))
            .filter(Book.id == book.book_id).first()
        )
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")

        if not result.author:
            raise HTTPException(
                status_code=404, detail="Author not foundf for this book"
            )

        user = self.session.query(Users).filter(Users.user_id == user.user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.user_id != result.author.user_id:
            raise HTTPException(status_code=403, detail="Permission denied")

        if result.author_id != result.author.author_id:
            raise HTTPException(status_code=403, detail="This book has another author")

        result.is_published = True  # type:ignore
        self.session.commit()
        return {"Message": "Book is published"}
