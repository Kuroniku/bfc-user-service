import json
from typing import Type

from pydantic import ValidationError

from .base_http_exception import BaseHTTPException
from src.models import BaseModel


class UnknownError(BaseHTTPException):
    _message = f""
    _error_code = 1
    _status_code = 500

    def __init__(
            self,
            exception: Exception,
    ):
        super().__init__()
        self._message = f"Unhandled error {exception}"


class ValidationHTTPError(BaseHTTPException):
    _message = f""
    _error_code = 1
    _status_code = 422

    def __init__(
            self,
            exception: ValidationError
    ):
        super().__init__()
        self._message = []
        for error_info in exception.errors():
            self._message.append(
                {
                    "value": str(error_info['input']),
                    "field": str(error_info['loc'][-1]),
                    "message": error_info['msg'],
                }
            )


class EntityDoesNotExistError(BaseHTTPException):
    _message = f""
    _error_code = 2
    _status_code = 400

    def __init__(
            self,
            model_class: Type[BaseModel],
    ):
        super().__init__()
        self._message = f"Entity does not exist in table {model_class.__tablename__}"


class EntityAlreadyExistsError(BaseHTTPException):
    _message = f""
    _error_code = 3
    _status_code = 400

    def __init__(
            self,
            model_class: Type[BaseModel],
    ):
        super().__init__()
        self._message = f"Entity is already exist in table {model_class.__tablename__}"
