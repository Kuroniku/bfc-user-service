from src.models import UserModel
from src.dto import UserFullDTO
from src.repos import UserRepository
from src.service import UserService

user_repo = UserRepository(
    model=UserModel,
    dto=UserFullDTO
)

user_service = UserService(user_repo)


def get_user_service() -> UserService:
    return user_service
