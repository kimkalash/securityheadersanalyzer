from fastapi import FastAPI
from app.db import Base, engine
from app.routes import users, scans, auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(scans.router)
app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "Security Header Analyzer is running"}


