from app.utils.responses import success_response, error_response

def test_success_response():
    data = {"x": 1}
    resp = success_response(data)
    assert resp["success"] is True
    assert resp["data"] == data

def test_error_response():
    resp = error_response("404", "Not Found", {"missing": "user"})
    assert resp["success"] is False
    assert resp["error"]["code"] == "404"
    assert resp["error"]["message"] == "Not Found"
    assert resp["error"]["details"]["missing"] == "user"
