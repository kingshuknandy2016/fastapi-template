from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def create_user(self, payload: UserCreate):
        return self.user_repository.create_user(
            name=payload.name,
            email=payload.email,
            role=payload.role,
        )

    def update_user(self, user_id: int, payload: UserUpdate):
        data = payload.model_dump(exclude_unset=True)
        if not data:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            return user
        updated = self.user_repository.update_user(
            user_id,
            name=data.get("name"),
            email=data.get("email"),
            role=data.get("role"),
        )
        if updated is None:
            raise ValueError("User not found")
        return updated

    def delete_user(self, user_id: int) -> None:
        deleted = self.user_repository.delete_user(user_id)
        if not deleted:
            raise ValueError("User not found")
