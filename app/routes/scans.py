from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.security import get_current_user
from app.services.scan_service import create_scan, get_scans_for_user, delete_scan


router = APIRouter(prefix="/scans", tags=["scans"])

@router.post("/")
def create_new_scan(url: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # For now, just fake the result
    result = f"Headers analyzed for {url}"
    return create_scan(db, current_user.id, url, result)

@router.get("/")
def list_user_scans(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_scans_for_user(db, current_user.id)

@router.delete("/{scan_id}")
def remove_scan(scan_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_scan(db, scan_id)
