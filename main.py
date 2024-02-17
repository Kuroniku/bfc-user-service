import asyncio

import uvicorn

from src.db_repo import create_tables
from src.rest_app import app

if __name__ == "__main__":
    asyncio.run(create_tables())
    uvicorn.run(
        app,
        host="0.0.0.0"
    )
