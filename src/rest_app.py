from fastapi import FastAPI

from src.app import CustomApp
from src.handlers import extras_router, user_router, friends_relations_router, subscribe_relations_router
from src.repos import create_tables

app = CustomApp()


@app.on_event("startup")
async def create_db():
    await create_tables()


app.include_router(
    extras_router
)

app.include_router(
    user_router
)

app.include_router(
    friends_relations_router
)

app.include_router(
    subscribe_relations_router
)
