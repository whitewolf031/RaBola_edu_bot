from app.database.connection import db_manager
from app.core.logger import logger

def run_migrations():
    """Baza jadvallarini yaratish va yangilash"""
    try:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. users jadvali (til va foydalanuvchi ma'lumotlari)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        chat_id BIGINT PRIMARY KEY,
                        username VARCHAR(255),
                        full_name VARCHAR(255),
                        language VARCHAR(10) DEFAULT 'uz',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 2. Eski user_ids jadvali bo'lsa, ma'lumotlarni ko'chirish
                cursor.execute("""
                    DO $$
                    BEGIN
                        IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user_ids') THEN
                            INSERT INTO users (chat_id)
                            SELECT chat_id FROM user_ids
                            ON CONFLICT (chat_id) DO NOTHING;
                        END IF;
                    END
                    $$;
                """)

                # 3. applications jadvali (ro'yxatdan o'tganlar arizalari)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS applications (
                        id SERIAL PRIMARY KEY,
                        chat_id BIGINT,
                        full_name VARCHAR(255),
                        phone_number VARCHAR(50),
                        course_name VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

        logger.info("Ma'lumotlar bazasi migratsiyalari muvaffaqiyatli bajarildi.")
    except Exception as e:
        logger.error(f"Migratsiyalarni bajarishda xatolik: {e}")
