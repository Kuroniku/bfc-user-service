from typing import Callable

from fastapi import FastAPI
from fastapi.applications import AppType
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.app.base_http_exception import ErrorContent, BaseHTTPException
from src.app.http_exceptions import ValidationHTTPError, UnknownError

response_code_list = [400, 422, 500]
response_code_dict = {
    code: {
        "model": ErrorContent
    }
    for code in response_code_list
}


class CustomApp(FastAPI):
    def __init__(self: AppType, *args, **kwargs):
        if 'responses' not in kwargs:
            kwargs['responses'] = response_code_dict
        super().__init__(*args, **kwargs)

        self.add_exception_handler(RequestValidationError, self._handle_validation_error)
        self.add_exception_handler(BaseHTTPException, self._handle_base_http_exception)
        self.add_exception_handler(Exception, self._handle_unknown_error)

    @staticmethod
    def _handle_validation_error(request, exc):
        return ValidationHTTPError(exc).generate_response()

    @staticmethod
    def _handle_base_http_exception(request, exc):
        return exc.generate_response()

    @staticmethod
    def _handle_unknown_error(request, exc):
        return UnknownError(exc).generate_response()
