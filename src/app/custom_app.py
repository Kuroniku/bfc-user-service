from fastapi import FastAPI
from fastapi.applications import AppType


class CustomApp(FastAPI):
    def __init__(self: AppType, *args, **kwargs):
        super().__init__(**kwargs)
