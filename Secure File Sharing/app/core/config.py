import os

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    EMAIL_SECRET_KEY: str = os.getenv("EMAIL_SECRET_KEY", "verify_email_secret")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()
