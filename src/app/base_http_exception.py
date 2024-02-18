from pydantic import BaseModel
from fastapi.responses import JSONResponse


class ErrorContent(BaseModel):
    service_name: str
    message: str | list | dict
    error_code: int


class BaseHTTPException(Exception):
    _service_name = "user-service"
    _message = "Base Exception"
    _error_code = -1

    _status_code = 400

    class ErrorJSONResponse(JSONResponse):
        def __init__(
            self,
            _service_name: str,
            _message: str,
            _error_code: int,
            status_code: int
        ) -> None:
            content = ErrorContent(
                service_name=_service_name,
                message=_message,
                error_code=_error_code,
            ).dict()
            super().__init__(content, status_code)

    def __init__(self):
        exception_message = f'Service: {self._service_name}, Message: {self._message}, Error: {self._error_code}'
        super().__init__(
            exception_message
        )

    def generate_response(self):
        return self.ErrorJSONResponse(
            self._service_name,
            self._message,
            self._error_code,
            self._status_code
        )
