from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.db.database import SessionLocal
from app.core.security import create_access_token
from app.db import models
from app.core.email_utils import generate_verification_token, verify_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(email: str, password: str, role: str, db: Session = Depends(get_db)):
    print(f"📥 Signup attempt: {email}, {role}")
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = pwd_context.hash(password)
        new_user = models.User(email=email, hashed_password=hashed_pw, role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("✅ Signup successful")
        return {"message": "Signup successful"}
    except Exception as e:
        print(f"❌ Signup Error: {repr(e)}")  # 🔥 Log the actual error
        raise HTTPException(status_code=500, detail="Signup failed")


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/send-verification")
def send_verification_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = generate_verification_token(email)
    # In real-world: send email using SMTP or SendGrid
    verify_url = f"http://localhost:8000/auth/verify-email?token={token}"
    return {"message": "Verification link sent", "verify_url": verify_url}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_token(token)
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}
