from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException


class APIException(Exception):
    """Base class for personalized API Exceptions.

    :param Exception: Python Exception class.
    """

    def __init__(self, status: int, message: str):
        self.status_code = status
        self.message = message


# Exception creation/replacement
class ExceptionHandler:

    def __init__(self, app: FastAPI):
        app.exception_handler(Exception)(self.handler_exception)
        app.exception_handler(HTTPException)(self.handler_http_excep)
        app.exception_handler(APIException)(self.handler_api_exception)
        app.exception_handler(RequestValidationError)(self.handler_validation_exception)

    @staticmethod
    async def handler_exception(request: Request, exception: Exception):
        return JSONResponse(
            status_code=500, content={"message": 'Internal server error'}
        )

    @staticmethod
    async def handler_http_excep(request: Request, exception: HTTPException):
        default_http_responses = {404: "Not found",
                                  500: "Internal server error",
                                  400: "Bad request"}
        message = str(exception)
        if exception.status_code in default_http_responses.keys():
            message = default_http_responses[exception.status_code]
        return JSONResponse(
            status_code=exception.status_code,
            content={"message": message}
        )

    @staticmethod
    async def handler_api_exception(request: Request, exception: APIException):
        return JSONResponse(
            status_code=exception.status_code,
            content={"message": exception.message}
        )

    @staticmethod
    async def handler_validation_exception(request: Request, exception: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "message": "Invalid request parameters.",
                "details": str(exception)
            }
        )
