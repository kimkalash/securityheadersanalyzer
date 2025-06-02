from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import create_user, get_user_by_id, update_user, delete_user

router = APIRouter()

class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password_hash: str

class UserUpdateRequest(BaseModel):
    username: str | None = None
    email: str | None = None

# ✅ POST /users
@router.post("/users")
def register_user(data: UserRegisterRequest):
    try:
        user = create_user(data.username, data.email, data.password_hash)
        return {"message": "User created", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ GET /users/{user_id}
@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }


# ✅ PUT /users/{user_id}
@router.put("/users/{user_id}")
def update_user_route(user_id: int, data: UserUpdateRequest):
    try:
        update_user(user_id, data.username, data.email)
        return {"message": "User updated"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ✅ DELETE /users/{user_id}
@router.delete("/users/{user_id}")
def delete_user_route(user_id: int):
    try:
        delete_user(user_id)
        return {"message": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
