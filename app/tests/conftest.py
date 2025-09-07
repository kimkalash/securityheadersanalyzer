# conftest.py
import sys, os
import pytest
from app.db import Base, engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
