from .models import UserModel, FriendsRelationsModel, SubscribeRelationsModel, BaseModel
from .connection import async_engine


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

