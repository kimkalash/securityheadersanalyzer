from fastapi import FastAPI
from app.routes import users, scans
from app.services import analyze_headers  # import the service function
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.responses import error_response
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from app.routes import auth_routes

app = FastAPI()
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            code="http_error",
            message=exc.detail
        )
    )
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Transform Pydantic errors into a flat dictionary
    errors = {}
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if isinstance(loc, str))
        errors[field] = err["msg"]

    return JSONResponse(
        status_code=422,
        content=error_response(
            code="validation_error",
            message="Invalid input",
            details=errors
        )
    )
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
app.include_router(auth_routes.router)

