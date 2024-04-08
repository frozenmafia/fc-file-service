from fastapi import Depends, APIRouter, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from ..authentication.authenticatior import auth_required
import os
import uuid
from app import models

router = APIRouter(
    tags=["images"],
    prefix="/images"
)

@router.post("/upload")
async def uploadImage(
    image:UploadFile,
    current_user: models = Depends(auth_required),
):
    allowed_extensions = {'jpg','jpeg','png'}
    extension = image.filename.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only accepts JPEG, JPG and PNG")
    content = await image.read()
    
    filename = generate_unique_filename(image.filename)
    with open(f'uploads/images/{filename}','wb') as f:
        f.write(content)
        
    return {"access_url":f'{os.getenv("FILE_SERVICE_URL")}/images/{filename}'}
    
    
@router.get("/{filename:path}")  # Use path parameter for flexibility
async def get_image(filename: str):
    image_path = os.path.join('uploads/images', filename)

    if not os.path.isfile(image_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    file_extension = os.path.splitext(filename)[1].lower()  # Extract extension for media type
    media_type = {
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".png": "image/png",
        # Add more extensions as needed
    }.get(file_extension, "application/octet-stream")  # Default for unknown extensions

    return FileResponse(image_path, media_type=media_type)
 
    
def generate_unique_filename(original_filename):
    base, extension = os.path.splitext(original_filename)
    unique_id = str(uuid.uuid4())[:8]
    return f"{base}_{unique_id}{extension}" 