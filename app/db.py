from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # Make sure to import this

# Connect to your existing database file
engine = create_engine('sqlite:///../database.db', connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Ensure tables are created if not using Alembic migrations
Base.metadata.create_all(bind=engine)
