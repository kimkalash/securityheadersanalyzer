from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "secret"  # in production load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class SafeCryptContext(CryptContext):
    def hash(self, password, **kwargs):
        if isinstance(password, str):
            password = password.encode("utf-8")
        print(f"[DEBUG] Hashing password of length {len(password)}")
        if len(password) > 72:
            password = password[:72]
            print(f"[DEBUG] Password truncated to 72 bytes")
        return super().hash(password, **kwargs)

    def verify(self, password, hash, **kwargs):
        if isinstance(password, str):
            password = password.encode("utf-8")
        print(f"[DEBUG] Verifying password of length {len(password)}")
        if len(password) > 72:
            password = password[:72]
            print(f"[DEBUG] Password truncated to 72 bytes for verification")
        return super().verify(password, hash, **kwargs)


pwd_context = SafeCryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
    secret: str = SECRET_KEY,
    algorithm: str = ALGORITHM,
):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=algorithm)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


