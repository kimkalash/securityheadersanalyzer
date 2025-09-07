from sqlalchemy.orm import Session
from app.models import User
from app.core.security import get_password_hash

def register_user(db: Session, username: str, password: str, email: str) -> User:
    hashed_password = get_password_hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
