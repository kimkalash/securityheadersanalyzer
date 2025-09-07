from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.security import get_current_user
from app.services import scan_service   # ✅ import the whole module

router = APIRouter(prefix="/scans", tags=["scans"])

@router.post("/")
def create_new_scan(
    url: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    analysis_result = scan_service.analyze_headers(url)   # ✅ patched correctly
    scan = scan_service.create_scan(
        db, user_id=current_user.id, url=url, headers=analysis_result["headers"]
    )
    return {
        "scan_id": scan.id,
        "url": scan.url,
        "analysis": analysis_result["headers"],
        "created_at": scan.created_at,
    }

@router.get("/")
def list_scans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return scan_service.get_scans_for_user(db, current_user.id)

@router.delete("/{scan_id}")
def delete_scan_entry(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return scan_service.delete_scan(db, scan_id, current_user.id)
