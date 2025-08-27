import httpx
import json
from sqlalchemy.orm import Session
from app.models import Scan

def analyze_headers(url: str) -> dict:
    """
    Fetch a URL and analyze its security headers.
    Returns a dict with header statuses: strong, weak, or missing.
    """

    results = {}

    try:
        response = httpx.get(url, follow_redirects=True, timeout=10.0)
        headers = response.headers
    except Exception as e:
        return {"error": f"Failed to fetch {url}: {str(e)}"}

    # 1. Strict-Transport-Security (HSTS)
    hsts = headers.get("Strict-Transport-Security")
    if not hsts:
        results["Strict-Transport-Security"] = "missing"
    elif "max-age" in hsts:
        try:
            max_age = int(hsts.split("max-age=")[1].split(";")[0])
            if max_age >= 15768000 and "includesubdomains" in hsts.lower():
                results["Strict-Transport-Security"] = "strong"
            else:
                results["Strict-Transport-Security"] = "weak"
        except Exception:
            results["Strict-Transport-Security"] = "weak"
    else:
        results["Strict-Transport-Security"] = "weak"

    # 2. Content-Security-Policy (CSP)
    csp = headers.get("Content-Security-Policy")
    if not csp:
        results["Content-Security-Policy"] = "missing"
    elif "unsafe-inline" in csp or "*" in csp:
        results["Content-Security-Policy"] = "weak"
    else:
        results["Content-Security-Policy"] = "strong"

    # 3. X-Frame-Options (XFO)
    xfo = headers.get("X-Frame-Options")
    if not xfo:
        results["X-Frame-Options"] = "missing"
    elif xfo.upper() in ["DENY", "SAMEORIGIN"]:
        results["X-Frame-Options"] = "strong"
    else:
        results["X-Frame-Options"] = "weak"

    # 4. X-Content-Type-Options (XCTO)
    xcto = headers.get("X-Content-Type-Options")
    if not xcto:
        results["X-Content-Type-Options"] = "missing"
    elif xcto.lower() == "nosniff":
        results["X-Content-Type-Options"] = "strong"
    else:
        results["X-Content-Type-Options"] = "weak"

    # 5. Referrer-Policy
    refpol = headers.get("Referrer-Policy")
    if not refpol:
        results["Referrer-Policy"] = "missing"
    elif refpol.lower() in ["no-referrer", "same-origin", "strict-origin-when-cross-origin"]:
        results["Referrer-Policy"] = "strong"
    else:
        results["Referrer-Policy"] = "weak"

    # 6. Permissions-Policy
    ppol = headers.get("Permissions-Policy")
    if not ppol:
        results["Permissions-Policy"] = "missing"
    elif "*" in ppol:
        results["Permissions-Policy"] = "weak"
    else:
        results["Permissions-Policy"] = "strong"

    return {
        "url": url,
        "headers": results
    }


def create_scan(db: Session, user_id: int, url: str, headers: dict) -> Scan:
    """
    Create and persist a Scan record.
    Handles Postgres JSON and SQLite Text storage.
    """
    if isinstance(Scan.headers.type.python_type, str):  # SQLite with Text
        headers_to_store = json.dumps(headers)
    else:  # Postgres JSON
        headers_to_store = headers

    scan = Scan(url=url, user_id=user_id, headers=headers_to_store)
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan


def get_scans_for_user(db: Session, user_id: int):
    """
    Retrieve all scans belonging to a user.
    """
    return db.query(Scan).filter(Scan.user_id == user_id).all()


def delete_scan(db: Session, scan_id: int, user_id: int):
    """
    Delete a scan if it belongs to the user.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == user_id).first()
    if not scan:
        return {"error": "Scan not found"}
    db.delete(scan)
    db.commit()
    return {"message": "Scan deleted"}

