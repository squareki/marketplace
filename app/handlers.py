from urllib.request import Request

from app.exceptions import BaseError

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.exceptions import(
    BaseError,
    ObjectNotFoundError,
    DuplicateObjectError,
    InvalidDataError,
    )

async def base_error_handler(
    _: Request,
    exc: BaseError,
) -> JSONResponse:
    return JSONResponse({"code": exc.code, "message": exc.message}, status_code=exc.code)
    #raise HTTPException(status_code=exc.code, detail=exc.message)

HANDLED_EXCEPTIONS = (
    (ObjectNotFoundError, base_error_handler),
    (DuplicateObjectError, base_error_handler),
    (InvalidDataError, base_error_handler)
)

def setup_exception_handlers(app: FastAPI) -> None:
    """add all exception handlers"""
    for exc_cls, handler in HANDLED_EXCEPTIONS:
        app.add_exception_handler(exc_cls, handler)