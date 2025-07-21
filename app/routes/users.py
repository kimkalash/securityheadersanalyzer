from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import create_user, get_user_by_id, update_user, delete_user
from app.dependencies.auth import get_current_user
from app.models import User
from fastapi import Depends
from app.utils.responses import success_response


router = APIRouter()

# 🧾 Registration input: username, email, plain password (not hashed)
class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str  # ✅ Correct name, not password_hash

# 🛠️ User update input
class UserUpdateRequest(BaseModel):
    username: str | None = None
    email: str | None = None

# ✅ POST /users — Create a new user with hashed password
@router.post("/users")
def register_user(data: UserRegisterRequest):
    try:
        user = create_user(data.username, data.email, data.password)  # 🔐 password will be hashed inside
        return {"message": "User created", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/me")
def get_user(current_user: User = Depends(get_current_user)):
    user = get_user_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    

# ✅ PUT /users/{user_id} — Update username/email
@router.put("/users/{user_id}")
def update_user_route(user_id: int, data: UserUpdateRequest):
    try:
        update_user(user_id, data.username, data.email)
        return {"message": "User updated"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ✅ DELETE /users/{user_id} — Delete user by ID
@router.delete("/users/{user_id}")
def delete_user_route(user_id: int):
    try:
        delete_user(user_id)
        return {"message": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
