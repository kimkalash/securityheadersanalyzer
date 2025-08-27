from fastapi import FastAPI
from app.db import Base, engine
from app.routes import users, auth, scans

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(scans.router)


