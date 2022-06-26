from typing import Optional


class BaseError(Exception):
    code: int = 500
    message: Optional[str] = None

class ObjectNotFoundError(BaseError):
    code = 404
    message = "Item not found"

class DuplicateObjectError(BaseError):
    code = 400
    message = "Duplicate object found"

class InvalidDataError(BaseError):
    code = 400
    message = "Validation Failed"