from app.models import Base
from sqlalchemy import create_engine

# Create a SQLite database (you can change the path if you want)
engine = create_engine('sqlite:///database.db')

# Create all tables
Base.metadata.create_all(engine)

print("Database and tables created.")