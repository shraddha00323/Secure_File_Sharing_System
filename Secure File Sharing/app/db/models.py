from sqlalchemy import Column, String, Boolean, Integer
from app.db.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    role = Column(String)  # "ops" or "client"
