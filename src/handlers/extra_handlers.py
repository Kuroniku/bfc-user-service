from fastapi import APIRouter

extras_router = APIRouter(
    prefix="/extras",
    tags=["Extras"]
)


@extras_router.get("/is_alive")
async def is_alive():
    return
