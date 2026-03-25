class UserRepository:
    def __init__(self):
        # Simulating DB or external API
        self._users = {
            1: {"id": 1, "name": "Alice"},
            2: {"id": 2, "name": "Bob"},
        }

    def get_user_by_id(self, user_id: int):
        return self._users.get(user_id)
