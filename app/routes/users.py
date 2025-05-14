from fastapi import APIRouter
from app.services import create_user, get_user_by_id

router = APIRouter()

@router.post("/users")
def register_user(username: str, email: str, password_hash: str):
    user = create_user(username, email, password_hash)
    return {"message": "User created", "user": user.id}

@router.get("/users/{user_id}")
def read_user(user_id: int):
    user = get_user_by_id(user_id)
    if user:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }
    return {"error": "User not found"}
