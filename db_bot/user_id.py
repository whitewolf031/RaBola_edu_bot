from app.database.repositories.user_repo import user_repo
from app.database.migrations import run_migrations

class UserIDsDB:
    """Eski kod bilan moslikni saqlash uchun Wrapper klass"""
    def __init__(self):
        run_migrations()

    def create_table(self):
        run_migrations()

    def insert_user(self, chat_id):
        user_repo.upsert_user(chat_id=chat_id)

    def check_user_exists(self, chat_id):
        return user_repo.get_user(chat_id) is not None

    def get_all_users(self):
        return user_repo.get_all_users()