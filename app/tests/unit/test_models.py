import pytest
from app.models import User, Scan
from datetime import datetime

def test_user_model_fields():
    user = User(username="alice", email="alice@example.com", hashed_password="hashed")
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.hashed_password == "hashed"
    # Relationship should be empty initially
    assert user.scans == []

def test_scan_model_fields():
    scan = Scan(url="http://example.com", user_id=1, headers={"test": "ok"})
    assert scan.url == "http://example.com"
    assert scan.user_id == 1
    assert isinstance(scan.created_at, datetime)
    assert scan.headers == {"test": "ok"}
