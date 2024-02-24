from abc import abstractmethod
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repo import BaseCRUDRepo, AbstractBaseCRUDRepo
from src.models.models import UserModel
from src.dto import UserFullDTO, UserPutDTO, UserPatchDTO


class AbstractUserRepository(AbstractBaseCRUDRepo):
    @abstractmethod
    async def get_by_link(
            self,
            session: AsyncSession,
            link: str
    ) -> UserFullDTO:
        """

        :param session: Session to add it in DB
        :param link: Link of user entity to get

        :raises EntityDoesNotExists: Entity with that link does not exist

        :return: UserFullDTO
        """


class UserRepository(BaseCRUDRepo, AbstractUserRepository):
    _model: Type[UserModel]
    _full_dto: Type[UserFullDTO]

    def __init__(
            self,
            model: Type[UserModel],
            dto: Type[UserFullDTO]
    ):
        super().__init__(model, dto)

    async def create_new_entity_(
            self,
            session: AsyncSession,
            data: UserFullDTO
    ) -> UserModel:
        return await super().create_new_entity(session, data)

    async def get_by_id(
            self,
            session: AsyncSession,
            entity_id: int
    ) -> UserFullDTO:
        return await super().get_by_id(session, entity_id)

    async def update_from_dto(
            self,
            session: AsyncSession,
            entity_id: int,
            entity_data: UserPutDTO | UserPatchDTO
    ) -> UserFullDTO:
        return await super().update_from_dto(session, entity_id, entity_data)

    async def get_by_link(
            self,
            session: AsyncSession,
            link: str
    ) -> UserFullDTO:
        query = select(
            self._model
        ).where(
            self._model.profile_link == link
        )
        entity_generator = await session.execute(query)
        entity_list = entity_generator.scalars().all()
        if len(entity_list) == 0:
            raise self.EntityDoesNotExists(self._model)

        return self._create_dto(entity_list[0])
