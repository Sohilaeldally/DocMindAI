from fastapi import APIRouter,UploadFile, File
from app.config.settings import settings
from app.utils.file_validate import validate_file_type, validate_file_size
from pathlib import Path 
import uuid
import shutil
from app.models.document import Document
from app.db.document_repository import insert_document

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    validate_file_type(file.content_type)
    validate_file_size(file_size)

    file_id=uuid.uuid4()
    stored_name=f"{file_id}{Path(file.filename).suffix}"
    file_path= settings.UPLOAD_DIR / stored_name

    with open(file_path, "wb") as buffer:   
        shutil.copyfileobj(file.file,buffer)

    new_doc = Document(
        id=file_id,
        original_name=file.filename,
        stored_name=stored_name,
        content_type=file.content_type,
        file_size=file_size,
        status="uploaded"  
    )
    insert_document(new_doc)

    return {
        "message": "File uploaded successfully and metadata saved.",
        "id": str(file_id),
        "original_name": file.filename, 
        "stored_name": stored_name,
    }
  