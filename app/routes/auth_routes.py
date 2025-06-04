# app/routes/auth_routes.py

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from app.services import get_user_by_id
from app.auth.auth import verify_password, create_access_token
from app.services import SessionLocal
from app.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    session = SessionLocal()
    try:
        # Step 1: Find user by email
        user = session.query(User).filter(User.email == data.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Step 2: Check password
        if not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Step 3: Create token
        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    
    finally:
        session.close()
