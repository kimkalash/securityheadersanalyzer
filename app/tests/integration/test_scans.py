import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

client = TestClient(app)

# Fixture: reset DB for clean tests
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def register_and_login(username="eve", password="secret123", email="eve@example.com"):
    """Helper to register and login a user, returns auth headers."""
    client.post(
        "/users/",
        params={"username": username, "password": password, "email": email}
    )
    login_res = client.post(
        "/auth/login",
        params={"username": username, "password": password}
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_scan(monkeypatch):
    # Fake analyzer to avoid live HTTP call
    def fake_analyze_headers(url):
        return {"url": url, "headers": {"X-Frame-Options": "strong"}}

    monkeypatch.setattr("app.services.scan_service.analyze_headers", fake_analyze_headers)

    headers = register_and_login()

    res = client.post("/scans/", params={"url": "http://example.com"}, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["url"] == "http://example.com"
    assert data["analysis"]["X-Frame-Options"] == "strong"


def test_list_scans(monkeypatch):
    def fake_analyze_headers(url):
        return {"url": url, "headers": {"Referrer-Policy": "missing"}}

    monkeypatch.setattr("app.services.scan_service.analyze_headers", fake_analyze_headers)

    headers = register_and_login()

    # Create one scan
    client.post("/scans/", params={"url": "http://mysite.com"}, headers=headers)

    # List scans
    res = client.get("/scans/", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["url"] == "http://mysite.com"


def test_delete_scan(monkeypatch):
    def fake_analyze_headers(url):
        return {"url": url, "headers": {"Strict-Transport-Security": "weak"}}

    monkeypatch.setattr("app.services.scan_service.analyze_headers", fake_analyze_headers)

    headers = register_and_login()

    # Create a scan
    create_res = client.post("/scans/", params={"url": "http://delete.com"}, headers=headers)
    scan_id = create_res.json()["scan_id"]

    # Delete it
    delete_res = client.delete(f"/scans/{scan_id}", headers=headers)
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Scan deleted"

    # Verify deletion
    list_res = client.get("/scans/", headers=headers)
    assert list_res.status_code == 200
    assert list_res.json() == []
