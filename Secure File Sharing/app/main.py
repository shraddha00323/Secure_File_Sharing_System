from fastapi import FastAPI
from app.api.v1 import auth, ops_user, client_user

app = FastAPI()

# Include Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(ops_user.router, prefix="/ops")
app.include_router(client_user.router, prefix="/client")
from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)
