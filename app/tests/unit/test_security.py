import pytest
from jose import jwt
from app.core import security

# Use same secret & algorithm as config
SECRET = "testsecret"
ALGORITHM = "HS256"

def test_password_hash_and_verify():
    password = "supersecret"
    hashed = security.get_password_hash(password)

    # Hash should not equal raw password
    assert hashed != password  

    # Correct password should verify
    assert security.verify_password(password, hashed)

    # Wrong password should fail
    assert not security.verify_password("wrongpassword", hashed)


def test_create_access_token_and_decode():
    data = {"sub": "testuser"}
    token = security.create_access_token(data, secret=SECRET, algorithm=ALGORITHM)

    # Token should be a non-empty string
    assert isinstance(token, str)
    assert len(token) > 20

    # Decode the token using same secret/algorithm
    decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])

    # Payload should contain our subject
    assert decoded["sub"] == "testuser"
