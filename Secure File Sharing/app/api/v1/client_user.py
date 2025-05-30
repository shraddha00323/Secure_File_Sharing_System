from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException
from app.services.token_service import get_current_user, create_download_token
import os

router = APIRouter()

@router.get("/list-files")
def list_files(user=Depends(get_current_user)):
    if user["role"] != "client":
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"files": os.listdir("uploads/")}

@router.get("/download-link/{filename}")
def download_link(filename: str, user=Depends(get_current_user)):
    if user["role"] != "client":
        raise HTTPException(status_code=403, detail="Only clients can download")
    token = create_download_token(filename)
    return {"download-link": f"/client/download/{token}"}

@router.get("/download/{token}")
def download_file(token: str, user=Depends(get_current_user)):
    from itsdangerous import URLSafeSerializer, BadSignature
    s = URLSafeSerializer("download_secret")
    try:
        filename = s.loads(token)
    except BadSignature:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    if user["role"] != "client":
        raise HTTPException(status_code=403, detail="Not authorized")

    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
