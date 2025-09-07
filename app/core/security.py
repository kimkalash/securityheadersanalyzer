# app/services/scan_service.py
from sqlalchemy.orm import Session
from app.models import Scan
from datetime import datetime, timezone
import httpx


# Analyze headers
def analyze_headers(url: str) -> dict:
    try:
        response = httpx.get(url, follow_redirects=True, timeout=10.0)
        headers = response.headers
    except Exception as e:
        return {"error": str(e)}

    inspected = {
        "Strict-Transport-Security": evaluate_header("Strict-Transport-Security", headers.get("Strict-Transport-Security")),
        "Content-Security-Policy": evaluate_header("Content-Security-Policy", headers.get("Content-Security-Policy")),
        "X-Frame-Options": evaluate_header("X-Frame-Options", headers.get("X-Frame-Options")),
        "X-Content-Type-Options": evaluate_header("X-Content-Type-Options", headers.get("X-Content-Type-Options")),
        "Referrer-Policy": evaluate_header("Referrer-Policy", headers.get("Referrer-Policy")),
        "Permissions-Policy": evaluate_header("Permissions-Policy", headers.get("Permissions-Policy")),
    }

    return {"url": url, "headers": inspected}


# Helper to classify header value
def evaluate_header(name: str, value: str | None) -> str:
    if not value:
        return "missing"

    val = value.lower()

    # Strict-Transport-Security: must have long max-age
    if name == "Strict-Transport-Security":
        if "max-age" in val:
            try:
                age = int(val.split("max-age=")[1].split(";")[0])
                if age >= 31536000:
                    return "strong"
                else:
                    return "weak"
            except Exception:
                return "weak"
        return "weak"

    # X-Frame-Options
    if name == "X-Frame-Options":
        if val in ["deny", "sameorigin"]:
            return "strong"
        return "weak"

    # X-Content-Type-Options
    if name == "X-Content-Type-Options":
        if val == "nosniff":
            return "strong"
        return "weak"

    # Content-Security-Policy
    if name == "Content-Security-Policy":
        if "default-src" in val and "'self'" in val:
            return "strong"
        return "weak"

    # Referrer-Policy
    if name == "Referrer-Policy":
        if "no-referrer" in val or "strict-origin" in val:
            return "strong"
        return "weak"

    # Permissions-Policy
    if name == "Permissions-Policy":
        if "()" in val or val.strip() == "":
            return "strong"
        return "weak"

    return "weak"


# DB services
def create_scan(db: Session, user_id: int, url: str, headers: dict) -> Scan:
    scan = Scan(
        user_id=user_id,
        url=url,
        headers=headers,
        created_at=datetime.now(timezone.utc),  # ✅ fixed
    )
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
