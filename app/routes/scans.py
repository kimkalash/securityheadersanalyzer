from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth.auth import get_current_user
from app.services.scan_service import analyze_headers, create_scan, get_scans_for_user, delete_scan

router = APIRouter(prefix="/scans", tags=["scans"])

@router.post("/")
def create_new_scan(url: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    analysis_result = analyze_headers(url)
    scan = create_scan(db, user_id=current_user.id, url=url, headers=analysis_result["headers"])
    return {
        "scan_id": scan.id,
        "url": scan.url,
        "analysis": analysis_result["headers"],
        "created_at": scan.created_at
    }

@router.get("/")
def list_scans(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_scans_for_user(db, current_user.id)

@router.delete("/{scan_id}")
def delete_scan_entry(scan_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_scan(db, scan_id, current_user.id)
