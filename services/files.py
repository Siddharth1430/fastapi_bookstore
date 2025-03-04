from fastapi import HTTPException,UploadFile
from sqlalchemy.orm import Session
from dotenv import load_dotenv  
import cloudinary.uploader
import os
from fastapi.responses import StreamingResponse
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
class FileService:
    """This is a FileService class """
    def __init__(self,session: Session) -> None:
        """
        Constructor for CreateService
        """
        self.session = session 
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
        """_summary_
        This function is to stream a file.
        Args:
            file (UploadFile): File to be streamed.
        """
        def chunk():
            chunk_size =10 * 1024
            while True:
                chunk= file.read(chunk_size)
                if chunk:
                    yield chunk
        return StreamingResponse(chunk(), media_type="application/pdf")