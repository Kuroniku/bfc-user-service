from sqlalchemy.ext.asyncio import AsyncSession

from src.dto import UserFullDTO, UserPutDTO, UserPatchDTO
from src.repos import AbstractUserRepository


class UserService:
    _repo: AbstractUserRepository

    class EntityAlreadyExistsError(AbstractUserRepository.EntityAlreadyExists):
        message = f"Entity with that id is already exists in table Users"

        def __init__(self, model):
            super().__init__(model, self.message)

    class DuplicatesLinkError(AbstractUserRepository.DuplicatesOfUniqueFieldError):
        message = f"Duplicated link in table Users"

        def __init__(self, model, field):
            super().__init__(model, field, self.message)

    class EntityByIdDoesNotExistsError(AbstractUserRepository.EntityDoesNotExists):
        message = f"Entity with that id does not exists in table Users"

        def __init__(self, model):
            super().__init__(model, self.message)

    class EntityByLinkDoesNotExistsError(AbstractUserRepository.EntityDoesNotExists):
        message = f"Entity with that link does not exists in table Users"

        def __init__(self, model):
            super().__init__(model, self.message)

    def __init__(
            self,
            repo: AbstractUserRepository
    ):
        self._repo = repo

    async def create_user(
            self,
            session: AsyncSession,
            user: UserFullDTO,
    ) -> UserFullDTO:
        try:
            return await self._repo.create_new_entity(session, user)
        except self._repo.EntityAlreadyExists as e:
            raise self.EntityAlreadyExistsError(e.model)
        except self._repo.DuplicatesOfUniqueFieldError as e:
            raise self.DuplicatesLinkError(e.model, field="link")

    async def get_user_by_id(
            self,
            user_id: int,
            session: AsyncSession
    ) -> UserFullDTO:
        try:
            return await self._repo.get_by_id(session, user_id)
        except self._repo.EntityDoesNotExists as e:
            raise self.EntityByIdDoesNotExistsError(e.model)

    async def get_user_by_link(
            self,
            link: str,
            session: AsyncSession
    ):
        try:
            return await self._repo.get_by_link(session, link)
        except self._repo.EntityDoesNotExists as e:
            raise self.EntityByLinkDoesNotExistsError(e.model)

    async def update_user_by_id(
            self,
            user_id: int,
            user: UserPutDTO | UserPatchDTO,
            session: AsyncSession
    ):
        try:
            return await self._repo.update_from_dto(session, user_id, user)
        except self._repo.EntityDoesNotExists as e:
            raise self.EntityByIdDoesNotExistsError(e.model)

