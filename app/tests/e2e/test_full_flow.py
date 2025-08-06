from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_full_user_scan_flow():
    # 1. Register a new user
    username = "fullflowuser"
    password = "strongpassword"
    email = "fullflow@mail.com"
    response = client.post("/users/", json={
        "username": username,
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == username
    assert user_data["email"] == email

    # 2. Login with the user to get token
    response = client.post("/auth/login", data={
        "username": username,
        "password": password
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # 3. Create two scans
    urls = ["https://example1.com", "https://example2.com"]
    scan_ids = []
    for url in urls:
        resp = client.post("/scans/", params={"url": url}, headers=auth_headers)
        assert resp.status_code == 200
        scan = resp.json()
        assert scan["url"] == url
        scan_ids.append(scan["id"])

    # 4. List scans, verify both exist
    resp = client.get("/scans/", headers=auth_headers)
    assert resp.status_code == 200
    scans = resp.json()
    scan_urls = [scan["url"] for scan in scans]
    for url in urls:
        assert url in scan_urls

    # 5. Delete first scan
    resp = client.delete(f"/scans/{scan_ids[0]}", headers=auth_headers)
    assert resp.status_code == 200

    # 6. List scans again, verify first scan deleted, second remains
    resp = client.get("/scans/", headers=auth_headers)
    assert resp.status_code == 200
    scans = resp.json()
    scan_ids_after_delete = [scan["id"] for scan in scans]
    assert scan_ids[0] not in scan_ids_after_delete
    assert scan_ids[1] in scan_ids_after_delete
