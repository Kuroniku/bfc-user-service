from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import get_session
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
        session: AsyncSession = Depends(get_session)
) -> UserFullDTO:
    return await UserRepo.create_new_entity(session, user)


@user_router.get(
    path="/get-by-id"
)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_session)
) -> UserFullDTO:
    return await UserRepo.get_by_id(session, user_id)


@user_router.get(
    path="/get-by-link"
)
async def get_user(
        link: str,
        session: AsyncSession = Depends(get_session)
) -> UserFullDTO:
    return await UserRepo.get_by_link(session, link)


@user_router.put(
    path="/"
)
async def put_user_data(
        user_id: int,
        user: UserPutDTO,
        session: AsyncSession = Depends(get_session)
) -> UserFullDTO:
    return await UserRepo.update_from_dto(session, user_id, user)


@user_router.patch(
    path="/"
)
async def patch_user_data(
        user_id: int,
        user: UserPatchDTO,
        session: AsyncSession = Depends(get_session)
) -> UserFullDTO:
    return await UserRepo.update_from_dto(session, user_id, user)
