"""
Seed the users table. Run from project root after MySQL is up, e.g.:

  python -m scripts.seed_users

With Docker:

  docker compose run --rm app python -m scripts.seed_users
"""

from sqlalchemy import select, func

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.user import User

SEED_USER_COUNT = 50

# Distinct roles; assigned round-robin so each role appears across the set
ROLES = ("admin", "editor", "viewer", "analyst", "support")


def build_seed_rows(count: int) -> list[dict]:
    rows: list[dict] = []
    for i in range(1, count + 1):
        role = ROLES[(i - 1) % len(ROLES)]
        rows.append(
            {
                "name": f"Seed User {i:02d}",
                "email": f"seed{i:02d}@example.com",
                "role": role,
            }
        )
    return rows


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    default_rows = build_seed_rows(SEED_USER_COUNT)

    session = SessionLocal()
    try:
        count = session.scalar(select(func.count()).select_from(User))
        if count and count > 0:
            print("Users table already has data; skipping seed.")
            return

        for row in default_rows:
            session.add(
                User(name=row["name"], email=row["email"], role=row["role"])
            )
        session.commit()
        print(f"Seeded {len(default_rows)} users with roles: {', '.join(ROLES)}.")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
