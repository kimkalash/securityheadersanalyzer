from app.services import create_user, get_user_by_email, get_user_by_id
from fastapi import HTTPException
from app.db import SessionLocal
from app.models import User
from app.services import create_user, get_user_by_id, get_user_by_email
from fastapi import HTTPException
from app.controllers.user_controller import (
    register_user,
    fetch_user_by_id,
    delete_user_by_id,
)

def register_user(username: str, email: str, password: str):
    existing = get_user_by_email(email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    password_hash = f"hashed_{password}"

    user = create_user(username=username, email=email, password_hash=password_hash)

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
        }
    }


def fetch_user_by_id(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return delete_user_by_id(user_id)