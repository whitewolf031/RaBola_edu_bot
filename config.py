from app.core.config import settings

class Config:
    def __init__(self):
        self.db_bot()

    def db_bot(self):
        self.host = settings.DB_HOST
        self.user = settings.DB_USER
        self.db = settings.DB_NAME
        self.password = settings.DB_PASSWORD
        self.port = settings.DB_PORT
