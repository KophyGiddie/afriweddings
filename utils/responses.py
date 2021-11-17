def success_response(message="Data returned successfully", data=[]):
    return {"response_code": "100", "message": message, "results": data}


def error_response(message="An error occurred", response_code='101'):
    return {"response_code": response_code, "message": message}
