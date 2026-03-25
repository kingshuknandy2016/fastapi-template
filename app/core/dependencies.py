from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


class ServiceContainer:
    user_service: UserService | None = None


container = ServiceContainer()


def init_services():
    user_repo = UserRepository()
    container.user_service = UserService(user_repo)
