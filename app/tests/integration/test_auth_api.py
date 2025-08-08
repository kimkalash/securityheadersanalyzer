from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_success():
    client.post("/users/", json={
        "username": "charlie",
        "email": "charlie@mail.com",
        "password": "strongpass"
    })
    response = client.post("/auth/login", data={
        "username": "charlie",
        "password": "strongpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    client.post("/users/", json={
        "username": "daisy",
        "email": "daisy@mail.com",
        "password": "rightpass"
    })
    response = client.post("/auth/login", data={
        "username": "daisy",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    data = response.json()
    assert "Invalid credentials" in data["detail"]
