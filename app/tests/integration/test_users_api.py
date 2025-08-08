from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user_success():
    response = client.post("/users/", json={
        "username": "alice",
        "email": "alice@mail.com",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@mail.com"

def test_register_user_duplicate():
    client.post("/users/", json={
        "username": "bob",
        "email": "bob@mail.com",
        "password": "pass"
    })
    response = client.post("/users/", json={
        "username": "bob",
        "email": "bob2@mail.com",
        "password": "diffpass"
    })
    assert response.status_code == 400
    data = response.json()
    assert "Username already exists" in data["detail"]

