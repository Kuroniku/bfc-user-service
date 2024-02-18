from typing import Callable

from fastapi import FastAPI
from fastapi.applications import AppType
from fastapi.types import DecoratedCallable

from src.app.custom_http_exception import ErrorContent

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
