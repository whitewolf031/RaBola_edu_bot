from typing import Dict, Optional
from app.database.repositories.user_repo import user_repo
from app.core.logger import logger

class UserService:
    def __init__(self):
        # Tezkor kirish uchun in-memory cache
        self._lang_cache: Dict[int, str] = {}

    def get_language(self, chat_id: int) -> str:
        """Foydalanuvchi tilini olish: Avval keshdan, topilmasa DB dan"""
        if chat_id in self._lang_cache:
            return self._lang_cache[chat_id]
        
        lang = user_repo.get_language(chat_id)
        if lang not in ["uz", "ru", "en"]:
            lang = "uz"
        self._lang_cache[chat_id] = lang
        return lang

    def set_language(self, chat_id: int, lang: str):
        """Foydalanuvchi tilini DB da va keshda yangilash"""
        if lang not in ["uz", "ru", "en"]:
            lang = "uz"
        self._lang_cache[chat_id] = lang
        user_repo.update_language(chat_id, lang)
        logger.info(f"Foydalanuvchi {chat_id} tili muvaffaqiyatli saqlandi: {lang}")

    def register_user(self, chat_id: int, username: Optional[str] = None, full_name: Optional[str] = None, lang: str = "uz"):
        """Foydalanuvchini ro'yxatdan o'tkazish / bazada qayd etish"""
        current_lang = self.get_language(chat_id)
        lang_to_save = lang if lang in ["uz", "ru", "en"] else current_lang
        user_repo.upsert_user(chat_id, username, full_name, lang_to_save)
        self._lang_cache[chat_id] = lang_to_save

    def get_all_users(self):
        return user_repo.get_all_users()

    def get_users_count(self) -> int:
        return user_repo.get_users_count()

user_service = UserService()
