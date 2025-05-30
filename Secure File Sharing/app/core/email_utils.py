from itsdangerous import URLSafeTimedSerializer
from fastapi import HTTPException

SECRET = "verify_email_secret"
s = URLSafeTimedSerializer(SECRET)

def generate_verification_token(email):
    return s.dumps(email)

def verify_token(token, expiration=3600):
    try:
        email = s.loads(token, max_age=expiration)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return email
