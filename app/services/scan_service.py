import pytest
from app.services.scan_service import analyze_headers

def test_analyze_headers_missing_headers(monkeypatch):
    """Simulate a site with no security headers."""

    class FakeResponse:
        headers = {}

    def fake_get(url, follow_redirects=True, timeout=10.0):
        return FakeResponse()

    # Patch httpx.get to return fake response
    monkeypatch.setattr("app.services.scan_service.httpx.get", fake_get)

    result = analyze_headers("http://test.com")

    assert result["headers"]["Strict-Transport-Security"] == "missing"
    assert result["headers"]["Content-Security-Policy"] == "missing"
    assert result["headers"]["X-Frame-Options"] == "missing"

def test_analyze_headers_strong_headers(monkeypatch):
    """Simulate a site with all strong headers."""

    class FakeResponse:
        headers = {
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=()"
        }

    def fake_get(url, follow_redirects=True, timeout=10.0):
        return FakeResponse()

    monkeypatch.setattr("app.services.scan_service.httpx.get", fake_get)

    result = analyze_headers("http://secure.com")

    for status in result["headers"].values():
        assert status == "strong"


