from typing import Optional, List, Dict
from app.database.connection import db_manager
from app.core.logger import logger

class ApplicationRepository:
    def add_application(self, chat_id: int, full_name: str, phone_number: str, course_name: Optional[str] = None):
        """Ro'yxatdan o'tgan yangi arizani bazaga saqlash"""
        query = """
            INSERT INTO applications (chat_id, full_name, phone_number, course_name)
            VALUES (%s, %s, %s, %s);
        """
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (chat_id, full_name, phone_number, course_name))
            logger.info(f"Yangi ariza DB ga saqlandi: {full_name} ({phone_number})")
        except Exception as e:
            logger.error(f"Arizani saqlashda xatolik: {e}")

    def get_applications_count(self) -> int:
        """Arizalar umumiy soni"""
        query = "SELECT COUNT(*) FROM applications;"
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Arizalar sonini olishda xatolik: {e}")
            return 0

    def get_recent_applications(self, limit: int = 5) -> List[Dict]:
        """Oxirgi arizalarni olish"""
        query = """
            SELECT id, chat_id, full_name, phone_number, course_name, created_at
            FROM applications
            ORDER BY id DESC
            LIMIT %s;
        """
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (limit,))
                    rows = cursor.fetchall()
                    return [
                        {
                            "id": r[0],
                            "chat_id": r[1],
                            "full_name": r[2],
                            "phone_number": r[3],
                            "course_name": r[4],
                            "created_at": r[5]
                        }
                        for r in rows
                    ]
        except Exception as e:
            logger.error(f"Oxirgi arizalarni olishda xatolik: {e}")
            return []

app_repo = ApplicationRepository()
