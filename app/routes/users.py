from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.controllers.user_controller import register_user, read_user, fetch_user_by_id
from app.services import get_user_by_id
from app.db import SessionLocal
from app.models import User

router = APIRouter()

# ✅ Request schema for registration
class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str

# ✅ POST /users — Register a new user using controller logic
@router.post("/users")
def register_user_route(data: UserRegisterRequest):
    return register_user(
        username=data.username,
        email=data.email,
        password=data.password
    )

@router.get("/users/{user_id}")
def read_user(user_id: int):
    return fetch_user_by_id(user_id)

# ✅ DELETE /users/{user_id} — Delete user by ID
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"message": f"User {user_id} deleted"}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# ✅ PUT /users/{user_id} — Update user info
@router.put("/users/{user_id}")
def update_user(user_id: int, username: str = None, email: str = None):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if username:
            user.username = username
        if email:
            user.email = email
        session.commit()
        return {"message": "User updated", "user_id": user.id}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
