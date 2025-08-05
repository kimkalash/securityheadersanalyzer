from app.models import User

def test_user_fields():
    user = User(username="sam", email="s@mail.com", hashed_password="pass")
    assert user.username == "sam"
    assert user.email == "s@mail.com"
