from fastapi import APIRouter, HTTPException
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
