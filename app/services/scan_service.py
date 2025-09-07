# app/services/scan_service.py
# app/services/scan_service.py
from sqlalchemy.orm import Session
from app.models import Scan
from datetime import datetime
import httpx

# Analyze headers
def analyze_headers(url: str) -> dict:
    try:
        response = httpx.get(url, follow_redirects=True, timeout=10.0)
        headers = response.headers
    except Exception as e:
        return {"error": str(e)}

    inspected = {
        "Strict-Transport-Security": evaluate_header(headers.get("Strict-Transport-Security")),
        "Content-Security-Policy": evaluate_header(headers.get("Content-Security-Policy")),
        "X-Frame-Options": evaluate_header(headers.get("X-Frame-Options")),
        "X-Content-Type-Options": evaluate_header(headers.get("X-Content-Type-Options")),
        "Referrer-Policy": evaluate_header(headers.get("Referrer-Policy")),
        "Permissions-Policy": evaluate_header(headers.get("Permissions-Policy")),
    }

    return {"url": url, "headers": inspected}

# Helper to classify header value
def evaluate_header(value: str | None) -> str:
    if value is None:
        return "missing"
    val = value.lower()

    # Strict-Transport-Security: must have long max-age
    if "max-age" in val:
        try:
            age = int(val.split("max-age=")[1].split(";")[0])
            if age >= 31536000:
                return "strong"
            else:
                return "weak"
        except Exception:
            return "weak"

    if "deny" in val or "sameorigin" in val:
        return "strong"

    if val == "nosniff":
        return "strong"

    if "strict" in val or "'self'" in val:
        return "strong"

    return "weak"


# DB services
def create_scan(db: Session, user_id: int, url: str, headers: dict) -> Scan:
    scan = Scan(user_id=user_id, url=url, headers=headers, created_at=datetime.utcnow())
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

def get_scans_for_user(db: Session, user_id: int) -> list[Scan]:
    return db.query(Scan).filter(Scan.user_id == user_id).all()

def delete_scan(db: Session, scan_id: int, user_id: int) -> dict:
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == user_id).first()
    if not scan:
        return {"message": "Scan not found"}
    db.delete(scan)
    db.commit()
    return {"message": "Scan deleted"}

