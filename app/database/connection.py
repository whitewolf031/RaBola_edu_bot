import time
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from app.core.config import settings
from app.core.logger import logger

class DatabaseManager:
    _instance = None
    _pool: pool.ThreadedConnectionPool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._init_pool()
        return cls._instance

    def _init_pool(self):
        try:
            self._pool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                connect_timeout=10
            )
            logger.info("Ma'lumotlar bazasi bilan aloqa muvaffaqiyatli o'rnatildi (Connection Pool faol).")
        except Exception as e:
            logger.error(f"Ma'lumotlar bazasiga ulanishda xatolik: {e}")
            self._pool = None

    def get_pool(self):
        if self._pool is None:
            self._init_pool()
        return self._pool

    @contextmanager
    def get_connection(self):
        conn = None
        current_pool = self.get_pool()
        
        # Agar pool hali ham yo'q bo'lsa, to'g'ridan-to'g'ri ulanishga urinib ko'rish
        if current_pool is None:
            try:
                conn = psycopg2.connect(
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    database=settings.DB_NAME,
                    connect_timeout=10
                )
                yield conn
                conn.commit()
            except Exception as e:
                if conn:
                    conn.rollback()
                logger.error(f"DB xatoligi (to'g'ridan-to'g'ri): {e}")
                raise e
            finally:
                if conn:
                    conn.close()
            return

        try:
            conn = current_pool.getconn()
            # Ulanish tirikligini tekshirish
            if conn.closed:
                current_pool.putconn(conn, close=True)
                conn = psycopg2.connect(
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    database=settings.DB_NAME
                )
            yield conn
            conn.commit()
        except psycopg2.OperationalError as e:
            logger.warning(f"DB ulanishida uzilish, qayta ulanishga urinilmoqda: {e}")
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            # Qayta ulanishga urinish
            try:
                self._init_pool()
                if self._pool:
                    conn = self._pool.getconn()
                    yield conn
                    conn.commit()
            except Exception as retry_err:
                logger.error(f"DB qayta ulanishda xatolik: {retry_err}")
                raise retry_err
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            logger.error(f"DB xatoligi: {e}")
            raise e
        finally:
            if conn and current_pool:
                try:
                    current_pool.putconn(conn)
                except Exception:
                    pass

db_manager = DatabaseManager()
