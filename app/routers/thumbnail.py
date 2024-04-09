from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
import uuid
import os
from dotenv import load_dotenv
from app import models
from ..authentication.authenticatior import auth_required

load_dotenv()

router = APIRouter(
    tags=['thumbnails'],
    prefix="/thumbnails"   
)
@router.post("/upload")
async def uploadImage(
    image:UploadFile,
    current_user: models.User = Depends(auth_required)
):
    uploads_dir = "/uploads"

    allowed_extensions = {'jpg','jpeg','png'}
    extension = image.filename.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = "Only accepts JPEG,JPG, PNG")
    content = await image.read()
    
    filename = generate_unique_filename(image.filename)
    file_path = os.path.join(uploads_dir,"thumbnails", filename)
    with open(file_path,'wb') as f:
        f.write(content)
        
    return {"access_url":f'{os.getenv("FILE_SERVICE_URL")}/thumbnails/{filename}'}
    
@router.get("/{filename}")
async def getThumbnail(filename: str):
    image_path = os.path.join('/uploads/thumbnails', filename)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    return FileResponse(image_path, media_type='image/jpeg')  # Adjust media_t

def generate_unique_filename(original_filename):
    base, extension = os.path.splitext(original_filename)
    unique_id = str(uuid.uuid4())[:8]  # Generate unique identifier
    return f"{base}_{unique_id}{extension}"