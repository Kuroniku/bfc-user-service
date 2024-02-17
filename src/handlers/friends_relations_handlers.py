from fastapi import APIRouter

friends_relations_router = APIRouter(
    prefix="/friends",
    tags=["Friends"]
)
