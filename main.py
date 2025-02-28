from fastapi import FastAPI,Depends,Query,File,UploadFile
from services.retrieve import RetrieveService
from services.create import CreateService
from services.update import UpdateService
from services.delete import DeleteService
from services.users import UserService
from schemas import BookSchema,BookCreate,AuthorCreate,AuthorSchema,UserLogin,UserResponse,UserCreate,Refresh
from typing import List,Dict
from db import get_db 
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
#from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from auth import get_current_user

security = HTTPBearer()
app=FastAPI()

@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    results = UserService(db)
    return results.signup(user)
    
@app.post("/login")
def login_user(user :UserLogin ,db: Session= Depends(get_db)):
    results = UserService(db)
    return results.login_user(user)

@app.post("/auth/refresh")
def refresh(token : Refresh,db: Session= Depends(get_db)):
    results= UserService(db)
    return results.refresh(token)

@app.get("/")
def hello():
    """
    This function performs when no endpoints are given.
    Returns:
    Literal: Returns hello
    """
    return "hello"

@app.get("/books/all",response_model=List[BookSchema])
def get_books( db: Session = Depends(get_db)):
    results= RetrieveService(db)
    return results.get_books()

@app.get("/books",response_model=List[BookSchema])
def paginate_books(page_number: int=Query(1,gt=0),page_size: int =Query(5,lt=10),db: Session = Depends(get_db)):
    """
    This function performs when no specific endpoints are given.
    Returns:
     Returns all books in db
    """
    results = RetrieveService(db)
    return results.paginate_books(page_number,page_size)

@app.get("/books/{book_id}",response_model=BookSchema)
def get_individual_book(book_id : int, db: Session = Depends(get_db)):
    """
    This function performs when specific endpoints are given.
    validation:
        matches the given id with db.If no match found ,then execptation rises.
    Returns:
     Returns the specific book in db
    """    
    service = RetrieveService(db) 
    return service.get_individual_book(book_id)

@app.get("/authors", response_model=List[AuthorSchema])
def get_author(db: Session = Depends(get_db)):
    """
    This function performs when specific endpoints are given.
    validation:
        matches the given id with db.If no match found ,then execptation rises.
    Returns:
     Returns the specific book in db
    """
    service = RetrieveService(db)
    return service.get_author()

@app.post("/books/{book_id}/author", response_model=AuthorSchema)
def create_author(book_id : int,author_data: AuthorCreate, db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    """
    This function performs when specific endpoints are given.
    validation:
        matches the given id with db.If no match found ,then execptation rises.
    Returns:
     Returns the specific book in db
    """
    service = CreateService(db)
    return service.create_author(book_id,author_data,user)



@app.post("/books",response_model=BookSchema)
def create_book(book: BookCreate,db: Session= Depends(get_db),user: dict = Depends(get_current_user)):
    """
    This function creates the new book .
    validation:
        ensures no two books can have same title
    Returns:
        returns the book that is created.
        """

    service = CreateService(db) 
    return service.create_book(book,user)
    
@app.post("/files")
def upload_file(file:UploadFile = File(),db:Session = Depends(get_db),user: dict = Depends(get_current_user)):
    service = CreateService(db)
    return service.upload_file(file,user)

@app.post("/filestream")
def file_stream(file : UploadFile =File(),db:Session=Depends(get_db)):
    def iterfile():
        chunk_size =10 * 1024
        while True:
            chunk= file.read(chunk_size)
            if chunk:
                yield chunk
    return StreamingResponse(iterfile(), media_type="application/pdf")

@app.put("/books/{book_id}",response_model=BookSchema)
def update_book(book_id: int, book: BookCreate,db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    """
    This function updates the book by getting the id from user to locate the book.
    validation:
        matches the given id with db.If no match found ,then execptation rises.
        if user try to update the title to the existing one then exceptation rises
    Returns:
    returns the updated book
        """
    service = UpdateService(db) 
    return service.update_book(book_id,book,user)

@app.put("/authors/{author_id}", response_model=AuthorSchema)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    """
    This function updates the author by getting the id from user to locate the author.
    validation:
        matches the given id with db.If no match found ,then execptation rises.
        if user try to update the title to the existing one then exceptation rises
    Returns:
    returns the updated author
        """
    service = UpdateService(db)
    return service.update_author(author_id, author,user)


@app.delete("/books/{book_id}")
def delete_books(book_id : int,db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    """
    This function which gets the id of he book which needs to be deleted.
    Returns:
    Dict: return a dic to display a message
    """
    service = DeleteService(db) 
    return service.delete_book(book_id,user)

@app.delete("/authors/{author_id}")
def delete_author(author_id : int, db: Session = Depends(get_db),user: dict = Depends(get_current_user)):
    """
    This function which gets the id of the delete which needs to be deleted.
    Returns:
    Dict: return a dic to display a message
    """
    service = DeleteService(db)
    return service.delete_author(author_id,user)


