import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine, SessionLocal

client = TestClient(app)

# Fixture: reset DB for clean tests
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_login_success():
    # First register a user
    client.post(
        "/users/",
        params={"username": "charlie", "password": "secret123", "email": "charlie@example.com"}
    )

    # Then login
    response = client.post(
        "/auth/login",
        params={"username": "charlie", "password": "secret123"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure_wrong_password():
    # Register user
    client.post(
        "/users/",
        params={"username": "dave", "password": "secret123", "email": "dave@example.com"}
    )

    # Wrong password
    response = client.post(
        "/auth/login",
        params={"username": "dave", "password": "wrongpass"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_failure_unknown_user():
    response = client.post(
        "/auth/login",
        params={"username": "ghost", "password": "whatever"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
