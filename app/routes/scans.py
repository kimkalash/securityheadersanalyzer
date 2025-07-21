from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import run_scan_and_analyze, get_user_scans, delete_scan, update_scan
from app.dependencies.auth import get_current_user
from app.models import User
from fastapi import Depends
from app.utils.responses import success_response


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

@router.get("/scans")
def list_scans(current_user: User = Depends(get_current_user)):
    try:
        scans = get_user_scans(current_user)
        return success_response(scans)
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
