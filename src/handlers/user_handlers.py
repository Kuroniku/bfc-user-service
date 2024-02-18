from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import EntityAlreadyExistsError, EntityDoesNotExistError
from src.models import db_manager
from src.repos import UserRepo
from src.dto import UserFullDTO, UserPutDTO, UserPatchDTO

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.post(
    path="/"
)
async def create_user(
        user: UserFullDTO,
        session: AsyncSession = Depends(db_manager.get_session)
) -> UserFullDTO:
    try:
        return await UserRepo.create_new_entity(session, user)
    except UserRepo.EntityAlreadyExists as e:
        raise EntityAlreadyExistsError(e.model)


@user_router.get(
    path="/get-by-id"
)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(db_manager.get_session)
) -> UserFullDTO:
    try:
        return await UserRepo.get_by_id(session, user_id)
    except UserRepo.EntityDoesNotExists as e:
        raise EntityDoesNotExistError(e.model)


@user_router.get(
    path="/get-by-link"
)
async def get_user(
        link: str,
        session: AsyncSession = Depends(db_manager.get_session)
) -> UserFullDTO:
    try:
        return await UserRepo.get_by_link(session, link)
    except UserRepo.EntityDoesNotExists as e:
        raise EntityDoesNotExistError(e.model)


@user_router.put(
    path="/"
)
async def put_user_data(
        user_id: int,
        user: UserPutDTO,
        session: AsyncSession = Depends(db_manager.get_session)
) -> UserFullDTO:
    try:
        return await UserRepo.update_from_dto(session, user_id, user)
    except UserRepo.EntityDoesNotExists as e:
        raise EntityDoesNotExistError(e.model)


@user_router.patch(
    path="/"
)
async def patch_user_data(
        user_id: int,
        user: UserPatchDTO,
        session: AsyncSession = Depends(db_manager.get_session)
) -> UserFullDTO:
    try:
        return await UserRepo.update_from_dto(session, user_id, user)
    except UserRepo.EntityDoesNotExists as e:
        raise EntityDoesNotExistError(e.model)
