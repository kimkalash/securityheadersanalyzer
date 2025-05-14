from fastapi import APIRouter
from app.services import create_scan, get_user_scans

router = APIRouter()

@router.post("/scans")
def run_scan(user_id: int, url: str):
    scan = create_scan(user_id, url)
    return {"message": "Scan created", "scan_id": scan.id}

@router.get("/scans/{user_id}")
def list_user_scans(user_id: int):
    scans = get_user_scans(user_id)
    return [
        {
            "scan_id": s.id,
            "url": s.scan_url,
            "date": s.scan_date
        } for s in scans
    ]