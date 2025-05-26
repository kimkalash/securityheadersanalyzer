from app.services import run_scan_and_analyze, get_user_scans, delete_scan, update_scan
from app.routes.scans import ScanCreateRequest, ScanUpdateRequest

def register_scan(data: ScanCreateRequest):
    return run_scan_and_analyze(data.user_id, data.url)

def list_scans(user_id: int):
    return get_user_scans(user_id)

def remove_scan(scan_id: int):
    return delete_scan(scan_id)

def modify_scan(scan_id: int, data: ScanUpdateRequest):
    return update_scan(scan_id, data.url)
