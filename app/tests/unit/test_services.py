import pytest
from app import models
from app.services import create_user, get_user_by_id, create_scan

def test_create_user(db_session):
    user = create_user(db_session, "testuser", "test@example.com", "hashedpass")
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_get_user_by_id(db_session):
    user = create_user(db_session, "testuser2", "test2@example.com", "pass")
    found = get_user_by_id(db_session, user.id)
    assert found is not None
    assert found.id == user.id
