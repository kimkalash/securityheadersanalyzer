import pytest
from app.services.scan_service import analyze_headers

#
# 1. Missing headers
#
def test_analyze_headers_missing_headers(monkeypatch):
    class FakeResponse:
        headers = {}

    def fake_get(url, follow_redirects=True, timeout=10.0):
        return FakeResponse()

    monkeypatch.setattr("app.services.scan_service.httpx.get", fake_get)

    result = analyze_headers("http://test.com")

    assert result["headers"]["Strict-Transport-Security"] == "missing"
    assert result["headers"]["Content-Security-Policy"] == "missing"
    assert result["headers"]["X-Frame-Options"] == "missing"


#
# 2. Strong headers
#
def test_analyze_headers_strong_headers(monkeypatch):
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


#
# 3. Weak headers
#
def test_analyze_headers_weak_headers(monkeypatch):
    class FakeResponse:
        headers = {
            "Strict-Transport-Security": "max-age=1000",  # too short
            "Content-Security-Policy": "default-src *; script-src 'unsafe-inline'",
            "X-Frame-Options": "ALLOW-FROM http://example.com",  # weak
            "X-Content-Type-Options": "wrongvalue",
            "Referrer-Policy": "unsafe-url",
            "Permissions-Policy": "*"
        }

    def fake_get(url, follow_redirects=True, timeout=10.0):
        return FakeResponse()

    monkeypatch.setattr("app.services.scan_service.httpx.get", fake_get)

    result = analyze_headers("http://weak.com")

    for status in result["headers"].values():
        assert status == "weak"


#
# 4. Error handling (network failure)
#
def test_analyze_headers_network_error(monkeypatch):
    def fake_get(url, follow_redirects=True, timeout=10.0):
        raise Exception("Connection failed")

    monkeypatch.setattr("app.services.scan_service.httpx.get", fake_get)

    result = analyze_headers("http://broken.com")

    assert "error" in result
    assert "Connection failed" in result["error"]
