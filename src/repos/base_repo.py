from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel as BaseDTO
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BaseModel


class AbstractBaseCRUDRepo(ABC):
    _model: Type[BaseModel]
    _dto: Type[BaseDTO]

    def __init__(
            self,
            model: Type[BaseModel],
            dto: Type[BaseDTO]
    ):
        self._model = model
        self._dto = dto

    class EntityAlreadyExists(Exception):
        def __init__(self, _model, *args):
            super().__init__(*args)
            self.model = _model

    class DuplicatesOfUniqueFieldError(Exception):
        def __init__(self, _model, field_name, *args):
            super().__init__(*args)
            self.model = _model
            self.field_name = field_name

    class EntityDoesNotExists(Exception):
        def __init__(self, _model, *args):
            super().__init__(*args)
            self.model = _model

    @abstractmethod
    async def create_new_entity(
            self,
            session: AsyncSession,
            data: BaseDTO,
    ):
        """
        Create and add a new entity of model class

        :param session: Session to add it in DB
        :param data: DTO with data about model entity

        :raises EntityAlreadyExists: Entity with that id already exists
        :raises DuplicatesOfUniqueFieldError: Entity with any unique field already exists

        :return: DTO of new entity
        """

    @abstractmethod
    async def get_by_id(
            self,
            session: AsyncSession,
            entity_id: int
    ):
        """
        Get entity by id

        :param session: Session to add it in DB
        :param entity_id: id of entity to get

        :raises EntityDoesNotExists: entity with that id does not exist

        :return: DTO of entity
        """

    @abstractmethod
    async def update_from_dto(
            self,
            session: AsyncSession,
            entity_id: int,
            entity_data: BaseDTO
    ):
        """
        Update entity by id from data in DTO

        :param session: Session to add it in DB
        :param entity_id: id of entity to update
        :param entity_data: DTO with data about model entity

        :raises EntityDoesNotExists: entity with that id does not exist

        :return: DTO of entity
        """


class BaseCRUDRepo(AbstractBaseCRUDRepo):
    def _create_dto(self, entity):
        return self._dto.model_validate(entity, from_attributes=True)

    async def create_new_entity(
            self,
            session: AsyncSession,
            data: BaseDTO,
    ):
        new_entity = self._model(**data.dict())
        session.add(new_entity)
        try:
            await session.commit()
            return self._create_dto(new_entity)
        except IntegrityError as ex:
            await session.rollback()
            if "_pkey" in ex.args[0]:
                raise self.EntityAlreadyExists(self._model)
            elif "duplicate key value violates unique constraint" in ex.args[0]:
                raise self.DuplicatesOfUniqueFieldError(
                    self._model,
                    "foo"
                )
            else:
                raise ex
        except Exception as ex:
            await session.rollback()
            raise ex

    async def _get_by_id_entity(
            self,
            session: AsyncSession,
            entity_id: int
    ):
        query = select(
            self._model
        ).where(
            self._model.id == entity_id
        )
        entity_generator = await session.execute(query)
        entity_list = entity_generator.scalars().all()
        if len(entity_list) == 0:
            raise self.EntityDoesNotExists(self._model)
        return entity_list[0]

    async def get_by_id(
            self,
            session: AsyncSession,
            entity_id: int
    ):
        entity = await self._get_by_id_entity(session, entity_id)
        return self._create_dto(entity)

    async def update_from_dto(
            self,
            session: AsyncSession,
            entity_id: int,
            entity_data: BaseDTO
    ):
        # Good but dont work. Create issue to SQLAlchemy
        # await self.get_by_id(session, entity_id)
        # query = update(
        #     self._model
        # ).where(
        #     self._model.id == entity_id
        # ).values(
        #     **entity_data.dict()
        # )
        # await session.execute(query)
        entity = await self._get_by_id_entity(session, entity_id)
        for key, value in entity_data.dict().items():
            setattr(entity, key, value)
        await session.commit()

        return await self.get_by_id(session, entity_id)
