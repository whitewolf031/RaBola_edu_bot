from typing import Optional, List, Dict
from app.database.connection import db_manager
from app.core.logger import logger

class UserRepository:
    def upsert_user(self, chat_id: int, username: Optional[str] = None, full_name: Optional[str] = None, language: str = "uz"):
        """Foydalanuvchini bazaga qo'shish yoki ma'lumotlarini yangilash"""
        query = """
            INSERT INTO users (chat_id, username, full_name, language, updated_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (chat_id) DO UPDATE 
            SET username = COALESCE(EXCLUDED.username, users.username),
                full_name = COALESCE(EXCLUDED.full_name, users.full_name),
                updated_at = CURRENT_TIMESTAMP;
        """
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (chat_id, username, full_name, language))
        except Exception as e:
            logger.error(f"Foydalanuvchini saqlashda xatolik ({chat_id}): {e}")

    def update_language(self, chat_id: int, language: str):
        """Foydalanuvchi tanlagan tilni DB da saqlash/yangilash"""
        query = """
            INSERT INTO users (chat_id, language, updated_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (chat_id) DO UPDATE 
            SET language = EXCLUDED.language,
                updated_at = CURRENT_TIMESTAMP;
        """
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (chat_id, language))
            logger.info(f"Foydalanuvchi {chat_id} tili DB da '{language}' ga yangilandi.")
        except Exception as e:
            logger.error(f"Tilni yangilashda DB xatoligi ({chat_id}): {e}")

    def get_language(self, chat_id: int) -> str:
        """Foydalanuvchi tilini DB dan olish (topilmasa 'uz')"""
        query = "SELECT language FROM users WHERE chat_id = %s;"
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (chat_id,))
                    row = cursor.fetchone()
                    if row and row[0]:
                        return row[0]
        except Exception as e:
            logger.error(f"Tilni olishda DB xatoligi ({chat_id}): {e}")
        return "uz"

    def get_user(self, chat_id: int) -> Optional[Dict]:
        """Foydalanuvchi ma'lumotlarini olish"""
        query = "SELECT chat_id, username, full_name, language, created_at FROM users WHERE chat_id = %s;"
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (chat_id,))
                    row = cursor.fetchone()
                    if row:
                        return {
                            "chat_id": row[0],
                            "username": row[1],
                            "full_name": row[2],
                            "language": row[3],
                            "created_at": row[4]
                        }
        except Exception as e:
            logger.error(f"Foydalanuvchini olishda xatolik ({chat_id}): {e}")
        return None

    def get_all_users(self) -> List[int]:
        """Barcha foydalanuvchilarning chat_id larini olish"""
        query = "SELECT chat_id FROM users;"
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    return [row[0] for row in rows]
        except Exception as e:
            logger.error(f"Barcha foydalanuvchilarni olishda xatolik: {e}")
            return []

    def get_users_count(self) -> int:
        """Foydalanuvchilar umumiy sonini olish"""
        query = "SELECT COUNT(*) FROM users;"
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Foydalanuvchilar sonini olishda xatolik: {e}")
            return 0

user_repo = UserRepository()
