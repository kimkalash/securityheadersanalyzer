# app/services/scan_service.py

import httpx
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Scan

# Security baseline rules (very simplified version)
def evaluate_header(name: str, value: str | None) -> str:
    if not value:
        return "missing"

    # HSTS
    if name == "Strict-Transport-Security":
        return "strong" if "max-age=" in value and "31536000" in value else "weak"

    # CSP
    if name == "Content-Security-Policy":
        return "strong" if "'self'" in value or "default-src" in value else "weak"

    # X-Frame-Options
    if name == "X-Frame-Options":
        return "strong" if value.upper() in ["DENY", "SAMEORIGIN"] else "weak"

    # X-Content-Type-Options
    if name == "X-Content-Type-Options":
        return "strong" if value.lower() == "nosniff" else "weak"

    # Referrer-Policy
    if name == "Referrer-Policy":
        return "strong" if "strict" in value.lower() else "weak"

    # Permissions-Policy
    if name == "Permissions-Policy":
        return "strong" if value != "*" else "weak"

    return "weak"


def analyze_headers(url: str) -> dict:
    """Fetch a URL and analyze its security headers."""
    try:
        response = httpx.get(url, follow_redirects=True, timeout=10.0)
        headers = response.headers
    except Exception as e:
        return {"url": url, "error": str(e)}

    results = {}
    im


