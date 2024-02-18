from src.models import (BaseModel, UserModel, async_engine)
# , FriendsRelationsModel, SubscribeRelationsModel, async_engine)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        # await conn.close()

