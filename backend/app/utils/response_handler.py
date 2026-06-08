from fastapi.responses import JSONResponse


def json_response(data: dict, status_code: int = 200):
    return JSONResponse(status_code=status_code, content=data)
