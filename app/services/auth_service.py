from sqlalchemy.orm import Session
from app.models import User
from app.core.security import verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(db: Session, username: str, password: str) -> dict | None:
    user = authenticate_user(db, username, password)
    if not user:
        return None

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)

    return {"access_token": token, "token_type": "bearer"}
