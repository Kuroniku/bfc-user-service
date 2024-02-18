from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repo import BaseRepo
from src.models.models import UserModel
from src.dto import UserFullDTO


class UserRepo(BaseRepo):
    _model = UserModel
    _dto = UserFullDTO

    @classmethod
    async def create_new_entity_(
            cls,
            session: AsyncSession,
            data: UserFullDTO
    ) -> UserModel:
        return await super().create_new_entity(session, data)

    @classmethod
    async def get_by_id(
            cls,
            session: AsyncSession,
            entity_id: int
    ) -> UserFullDTO:
        return await super().get_by_id(session, entity_id)

    @classmethod
    async def get_by_link(
            cls,
            session: AsyncSession,
            link: str
    ) -> UserFullDTO:
        query = select(
            cls._model
        ).where(
            cls._model.profile_link == link
        )
        entity_generator = await session.execute(query)
        entity_list = entity_generator.scalars().all()
        if len(entity_list) == 0:
            raise cls.EntityDoesNotExists(cls._model)

        return cls._create_dto(entity_list[0])
