from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import EntityAlreadyExistsError, EntityDoesNotExistError, DuplicateEntityError
from src.depends import get_user_service
from src.models import db_manager
from src.repos import UserRepository
from src.dto import UserFullDTO, UserPutDTO, UserPatchDTO
from src.service import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.post(
    path="/"
)
async def create_user(
        user: UserFullDTO,
        session: AsyncSession = Depends(db_manager.get_session),
        user_service: UserService = Depends(get_user_service)
) -> UserFullDTO:
    try:
        return await user_service.create_user(session, user)
    except user_service.EntityAlreadyExistsError as e:
        raise EntityAlreadyExistsError(e.model)
    except user_service.DuplicatesLinkError as e:
        raise DuplicateEntityError(e.model, fieldname=e.field_name)


@user_router.get(
    path="/get-by-id"
)
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(db_manager.get_session),
        user_service: UserService = Depends(get_user_service)
) -> UserFullDTO:
    try:
        return await user_service.get_user_by_id(user_id, session)
    except user_service.EntityByIdDoesNotExistsError as e:
        raise EntityDoesNotExistError(e.model)


@user_router.get(
    path="/get-by-link"
)
async def get_user_by_link(
        link: str,
        session: AsyncSession = Depends(db_manager.get_session),
        user_service: UserService = Depends(get_user_service)
) -> UserFullDTO:
    try:
        return await user_service.get_user_by_link(link, session)
    except user_service.EntityByLinkDoesNotExistsError as e:
        raise EntityDoesNotExistError(e.model)


@user_router.put(
    path="/"
)
async def put_user_data(
        user_id: int,
        user: UserPutDTO,
        session: AsyncSession = Depends(db_manager.get_session),
        user_service: UserService = Depends(get_user_service)
) -> UserFullDTO:
    try:
        return await user_service.update_user_by_id(user_id, user, session)
    except user_service.EntityByIdDoesNotExistsError as e:
        raise EntityDoesNotExistError(e.model)


@user_router.patch(
    path="/"
)
async def patch_user_data(
        user_id: int,
        user: UserPatchDTO,
        session: AsyncSession = Depends(db_manager.get_session),
        user_service: UserService = Depends(get_user_service)
) -> UserFullDTO:
    try:
        return await user_service.update_user_by_id(user_id, user, session)
    except user_service.EntityByIdDoesNotExistsError as e:
        raise EntityDoesNotExistError(e.model)
