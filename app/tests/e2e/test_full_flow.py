import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

client = TestClient(app)

# Fixture: clean DB
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_full_user_flow(monkeypatch):
    # --- Step 1: Register ---
    register_res = client.post(
        "/users/",
        params={"username": "zoe", "password": "secret123", "email": "zoe@example.com"}
    )
    assert register_res.status_code == 200
    user_data = register_res.json()
    assert user_data["username"] == "zoe"

    # --- Step 2: Login ---
    login_res = client.post(
        "/auth/login",
        params={"username": "zoe", "password": "secret123"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Monkeypatch analyzer (so test doesn’t hit real websites)
    def fake_analyze_headers(url):
        return {"url": url, "headers": {"Content-Security-Policy": "strong"}}

    monkeypatch.setattr("app.services.scan_service.analyze_headers", fake_analyze_headers)

    # --- Step 3: Submit Scan ---
    scan_res = client.post("/scans/", params={"url": "http://e2e.com"}, headers=headers)
    assert scan_res.status_code == 200
    scan_data = scan_res.json()
    scan_id = scan_data["scan_id"]
    assert scan_data["analysis"]["Content-Security-Policy"] == "strong"

    # --- Step 4: Retrieve Scans ---
    list_res = client.get("/scans/", headers=headers)
    assert list_res.status_code == 200
    scans = list_res.json()
    assert len(scans) == 1
    assert scans[0]["url"] == "http://e2e.com"

    # --- Step 5: Delete Scan ---
    delete_res = client.delete(f"/scans/{scan_id}", headers=headers)
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Scan deleted"

    # Confirm deletion
    list_res2 = client.get("/scans/", headers=headers)
    assert list_res2.json() == []
