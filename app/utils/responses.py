# app/utils/responses.py

def error_response(code: str, message: str, details: dict = None) -> dict:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        }
    }

def success_response(data: dict | list | None = None) -> dict:
    return {
        "success": True,
        "data": data
    }
