from fastapi import FastAPI,Depends,Query,File,UploadFile
from services.retrieve import RetrieveService
from services.create import CreateService
from services.update import UpdateService
from services.delete import DeleteService
from services.users import UserService
from otp_auth.handler import OTPAuthentication
from schemas.author_schemas import AuthorCreate,AuthorSchema
from schemas.book_schemas import BookSchema,BookCreate,BookFilter
from schemas.user_schema import UserLogin,UserResponse,UserCreate,Refresh
from otp_auth.schema import Verifier,OTPGenerator
from typing import List
from db import get_db 
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer
from auth import get_current_user

security = HTTPBearer()
app=FastAPI()

@app.post("/generateotp")
def generate_otp(payload:OTPGenerator,db : Session= Depends(get_db)):
    """_summary_
    Generates an OTP for phone number authentication.
    Args:
        payload (GenerateOTP): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    Returns:
        _type_: str_
    """
    results = OTPAuthentication(db)
    return results.generate_otp(payload)

@app.post("/verify")
def verify_via_phone_number(payload:Verifier,db: Session= Depends(get_db)):
    """_summary_
     Verifies the OTP sent to the user's phone number.
    Args:
        payload (VerifyByPhoneNumber): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    Returns:
        dict: access token and refresh token
    """
    results = OTPAuthentication(db)
    return results.verify_via_phone_number(payload)

@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """_summary_
    Registers a new user and returns user details.
    Args:
        user (UserCreate): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    Returns:
        _type_: User pydantic model
    """
    results = UserService(db)
    return results.signup(user)
    
@app.post("/login")
def login_user(user :UserLogin ,db: Session= Depends(get_db)):
    """_summary_
    Authenticates a user and returns an access token.
    Args:
        user (UserLogin): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    Returns:
        _type_: dict
    """
    results = UserService(db)
    return results.login_user(user)

@app.post("/auth/refresh")
def refresh(token : Refresh,db: Session= Depends(get_db)):
    """_summary_
    Refreshes the authentication token.
    Args:
        token (Refresh): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    Returns:
        _type_: dict
    """
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
    """_summary_
    
    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).
    Returns:
        _type_:List of Book pydantic model
    """
    results= RetrieveService(db)
    return results.get_books()

@app.get("/users/all",response_model=List[UserResponse])
def get_users( db: Session = Depends(get_db)):
    """_summary_
    This function displays all users.
    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).
    Returns:
        _type_: List of User pydantic model
    """
    results= RetrieveService(db)
    return results.get_users()

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

@app.get("/books/",response_model=List[BookSchema])
def get_filtered_books(book : BookFilter = Depends(),db : Session = Depends(get_db)):
    """_summary_
    This function filters the book based on given query
    Args:
        book (BookFilter, optional): _description_. Defaults to Depends().
        db (Session, optional): _description_. Defaults to Depends(get_db).
    Returns:
        _type_: List of Bookschema
    """
    service = RetrieveService(db) 
    return service.get_filtered_books(book)

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
    """_summary_
    This function uploads file to cloudinary.
    Args:
        file (UploadFile, optional): _description_. Defaults to File().
        db (Session, optional): _description_. Defaults to Depends(get_db).
        user (dict, optional): _description_. Defaults to Depends(get_current_user).
    Returns:
        _type_: dict
    """
    service = CreateService(db)
    return service.upload_file(file,user)

@app.post("/filestream")
def file_stream(file : UploadFile =File(),db:Session=Depends(get_db)):
    """_summary_
    This function is to stream the file
    Args:
        file (UploadFile, optional): _description_. Defaults to File().
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
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

@app.put("/users/{user_id}", response_model= UserResponse)
def update_user(user_id : int, users : UserCreate, db: Session = Depends(get_db),user : dict= Depends(get_current_user)):
    """
    This function updates the  user credential.
    validation:
        matches the given credentials with db.If no match found ,then execptation rises.
    Returns:
    returns the updated user
        """
    service = UpdateService(db)
    return service.update_user(user_id,users,user)

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


