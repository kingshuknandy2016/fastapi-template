"""
Run all seed scripts in order. Usage:

  python -m scripts.seed_all

With Docker:

  docker compose run --rm app python -m scripts.seed_all
"""

from scripts.seed_users import seed as seed_users


def main() -> None:
    seed_users()


if __name__ == "__main__":
    main()
