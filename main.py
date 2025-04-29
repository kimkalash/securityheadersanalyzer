from fastapi import FastAPI

# Create the FastAPI app
app = FastAPI()

# Placeholder test route
@app.get("/")
def read_root():
    return {"message": "Security Headers Analyzer is live"}
