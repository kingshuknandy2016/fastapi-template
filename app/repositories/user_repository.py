from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def _to_dict(self, user: User) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }

    def get_user_by_id(self, user_id: int) -> dict | None:
        user = self._db.get(User, user_id)
        if user is None:
            return None
        return self._to_dict(user)

    def get_all_users(self) -> list[dict]:
        stmt = select(User).order_by(User.id)
        rows = self._db.scalars(stmt).all()
        return [self._to_dict(u) for u in rows]

    def email_exists(self, email: str, exclude_user_id: int | None = None) -> bool:
        stmt = select(User.id).where(User.email == email)
        if exclude_user_id is not None:
            stmt = stmt.where(User.id != exclude_user_id)
        return self._db.scalar(stmt) is not None

    def create_user(self, name: str, email: str, role: str) -> dict:
        if self.email_exists(email):
            raise ValueError("Email already registered")
        user = User(name=name, email=email, role=role)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return self._to_dict(user)

    def update_user(
        self,
        user_id: int,
        *,
        name: str | None = None,
        email: str | None = None,
        role: str | None = None,
    ) -> dict | None:
        user = self._db.get(User, user_id)
        if user is None:
            return None
        if email is not None and email != user.email and self.email_exists(
            email, exclude_user_id=user_id
        ):
            raise ValueError("Email already registered")
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if role is not None:
            user.role = role
        self._db.commit()
        self._db.refresh(user)
        return self._to_dict(user)

    def delete_user(self, user_id: int) -> bool:
        user = self._db.get(User, user_id)
        if user is None:
            return False
        self._db.delete(user)
        self._db.commit()
        return True
