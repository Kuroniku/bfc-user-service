from pydantic import BaseModel as BaseDTO
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BaseModel


class BaseRepo:
    _model = BaseModel
    _dto = BaseDTO

    class EntityAlreadyExists(Exception):
        def __init__(self, _model, *args):
            super().__init__(*args)
            self.model = _model

    class EntityDoesNotExists(Exception):
        def __init__(self, _model, *args):
            super().__init__(*args)
            self.model = _model

    @classmethod
    def _create_dto(cls, entity):
        return cls._dto.model_validate(entity, from_attributes=True)

    @classmethod
    async def create_new_entity(
            cls,
            session: AsyncSession,
            data: BaseDTO,
    ):
        new_entity = cls._model(**data.dict())
        session.add(new_entity)
        try:
            await session.commit()
            return cls._create_dto(new_entity)
        except IntegrityError:
            await session.rollback()
            raise cls.EntityAlreadyExists(cls._model)
        except Exception as ex:
            await session.rollback()
            raise ex

    @classmethod
    async def get_by_id(
            cls,
            session: AsyncSession,
            entity_id: int
    ):
        query = select(
            cls._model
        ).where(
            cls._model.id == entity_id
        )
        entity_generator = await session.execute(query)
        entity_list = entity_generator.scalars().all()
        if len(entity_list) == 0:
            raise cls.EntityDoesNotExists(cls._model)

        return cls._create_dto(entity_list[0])

    @classmethod
    async def update_from_dto(
            cls,
            session: AsyncSession,
            entity_id: int,
            entity_data: BaseDTO
    ):
        await cls.get_by_id(session, entity_id)
        query = update(
            cls._model
        ).where(
            cls._model.id == entity_id
        ).values(
            **entity_data.dict()
        )
        await session.execute(query)
        return await cls.get_by_id(session, entity_id)
