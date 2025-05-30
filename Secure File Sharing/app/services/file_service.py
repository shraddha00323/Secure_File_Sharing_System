import os
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads"
ALLOWED_EXT = ["pptx", "docx", "xlsx"]

def save_file(file: UploadFile):
    ext = file.filename.split(".")[-1]
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file.filename

def list_files():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    return os.listdir(UPLOAD_DIR)

def file_exists(filename: str):
    return os.path.exists(os.path.join(UPLOAD_DIR, filename))
