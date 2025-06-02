# app/utils/responses.py

def error_response(code: str, message: str, details: dict = None) -> dict:
    """
    Builds a standardized error response.

    Args:
        code (str): A machine-readable error code like 'user_not_found'.
        message (str): A human-readable explanation of the error.
        details (dict, optional): Optional extra context (e.g., which field failed).

    Returns:
        dict: A standardized error envelope for the frontend/API clients.
    """
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        }
    }
