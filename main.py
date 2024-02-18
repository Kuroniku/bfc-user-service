import asyncio

import uvicorn

# from src.repos import create_tables
from src.rest_app import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0"
    )
