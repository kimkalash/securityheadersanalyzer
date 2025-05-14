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

@router.delete("/scans/{scan_id}")
def delete_scan(scan_id: int):
    session = SessionLocal()
    try:
        scan = session.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        session.delete(scan)
        session.commit()
        return {"message": f"Scan {scan_id} deleted"}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
@router.put("/scans/{scan_id}")
def update_scan(scan_id: int, url: str):
    session = SessionLocal()
    try:
        scan = session.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        scan.scan_url = url
        session.commit()
        return {"message": "Scan updated", "scan_id": scan.id}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
