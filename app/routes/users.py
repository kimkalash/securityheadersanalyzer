from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import create_user, get_user_by_username
from app.auth.auth import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pw = hash_password(password)
    return create_user(db, username, email, hashed_pw)
