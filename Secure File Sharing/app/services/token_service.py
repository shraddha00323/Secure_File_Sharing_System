from fastapi import Depends, HTTPException
from jose import jwt
from app.core.security import decode_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

from itsdangerous import URLSafeSerializer
def create_download_token(filename: str):
    s = URLSafeSerializer("download_secret")
    return s.dumps(filename)
