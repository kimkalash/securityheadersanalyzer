from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_token():
    # Register and login user to get token
    username = "eve"
    password = "evesecret"
    client.post("/users/", json={
        "username": username,
        "email": "eve@mail.com",
        "password": password
    })
    resp = client.post("/auth/login", data={
        "username": username,
        "password": password
    })
    return resp.json()["access_token"]

def test_create_and_list_scan():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Create a scan
    response = client.post("/scans/", params={"url": "https://example.com"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["url"] == "https://example.com"
    # List scans
    response = client.get("/scans/", headers=headers)
    assert response.status_code == 200
    scans = response.json()
    assert isinstance(scans, list)
    assert any(scan["url"] == "https://example.com" for scan in scans)

def test_delete_scan():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Create a scan
    response = client.post("/scans/", params={"url": "https://deleteme.com"}, headers=headers)
    scan_id = response.json()["id"]
    # Delete the scan
    response = client.delete(f"/scans/{scan_id}", headers=headers)
    assert response.status_code == 200
    # Ensure it's gone
    response = client.get("/scans/", headers=headers)
    scans = response.json()
    assert not any(scan["id"] == scan_id for scan in scans)
