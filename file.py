from fastapi import FastAPI, File, UploadFile, HTTPException
import cloudinary.uploader

app = FastAPI()

# Allowed file types and max size (10MB)
ALLOWED_FILE_TYPE = "application/pdf"
MAX_FILE_SIZE_MB = 10

@app.post("/upload/")
async def upload_book(file: UploadFile ):
    # Validate file type
    if file.content_type != ALLOWED_FILE_TYPE:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is allowed.")

    # Validate file size
    file_size = len(file.read())
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit.")

    # Reset file cursor after size check
    await file.seek(0)

    # Upload file to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(file.file, resource_type="raw")
        return {"message": "File uploaded successfully", "url": upload_result["secure_url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
