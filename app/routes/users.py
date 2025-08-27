from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.user_service import register_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def register(username: str, password: str, email: str, db: Session = Depends(get_db)):
    return register_user(db, username, password, email)

