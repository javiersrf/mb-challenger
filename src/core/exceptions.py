
from fastapi.exceptions import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=400, detail=detail)