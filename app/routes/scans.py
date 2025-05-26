from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import run_scan_and_analyze, get_user_scans, delete_scan, update_scan

router = APIRouter()

# ✅ Request schema
class ScanCreateRequest(BaseModel):
    user_id: int
    url: str

class ScanUpdateRequest(BaseModel):
    url: str

# ✅ POST /scans — Full scan
@router.post("/scans")
def create_scan_route(data: ScanCreateRequest):
    try:
        result = run_scan_and_analyze(data.user_id, data.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ GET /scans/{user_id}
@router.get("/scans/{user_id}")
def list_scans(user_id: int):
    try:
        return get_user_scans(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ✅ DELETE /scans/{scan_id}
@router.delete("/scans/{scan_id}")
def delete_scan_route(scan_id: int):
    try:
        delete_scan(scan_id)
        return {"message": f"Scan {scan_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ✅ PUT /scans/{scan_id}
@router.put("/scans/{scan_id}")
def update_scan_route(scan_id: int, data: ScanUpdateRequest):
    try:
        update_scan(scan_id, data.url)
        return {"message": "Scan updated"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
