from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.services.token_service import get_current_user
import os

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    if user["role"] != "ops":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    allowed_exts = ["pptx", "docx", "xlsx"]
    if file.filename.split(".")[-1] not in allowed_exts:
        raise HTTPException(status_code=400, detail="Invalid file type")

    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}
