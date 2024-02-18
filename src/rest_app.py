import contextlib

from src.app import CustomApp
from src.handlers import extras_router, user_router, friends_relations_router, subscribe_relations_router
from src.models import db_manager


@contextlib.asynccontextmanager
async def create_db(app):
    db_manager.init()
    await db_manager.create_tables()
    yield
    await db_manager.close()


app = CustomApp(lifespan=create_db)

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
