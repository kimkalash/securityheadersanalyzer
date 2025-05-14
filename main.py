from fastapi import FastAPI
from app.routes import users, scans
from app.services import analyze_headers  # import the service function

app = FastAPI()

# Register routers
app.include_router(users.router)
app.include_router(scans.router)

@app.get("/")
def read_root():
    return {"message": "Security Headers Analyzer is live"}

@app.get("/analyze")
def analyze(url: str):
    result = analyze_headers(url)
    return {"result": result}