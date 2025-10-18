def format_response(status: str, message: str, data=None):
    return {
        "status": status,
        "message": message,
        "data": data
    }
