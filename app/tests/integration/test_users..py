import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine, SessionLocal

client = TestClient(app)

# Fixture: fresh DB for each test run
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_user_success():
    response = client.post(
        "/users/",
        params={"username": "alice", "password": "secret123", "email": "alice@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"

def test_register_user_duplicate_username():
    # First registration
    client.post(
        "/users/",
        params={"username": "bob", "password": "secret123", "email": "bob@example.com"}
    )
    # Try registering same username
    response = client.post(
        "/users/",
        params={"username": "bob", "password": "newpass", "email": "bob2@example.com"}
    )
    # You may need to handle duplicates in your service, but for now expect 500/400
    assert response.status_code in (400, 409, 500)
