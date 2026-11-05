import os
from typing import List
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

class Settings:
    # Telegram Bot sozlamalari
    BOT_TOKEN: str = os.getenv("TOKEN") or os.getenv("BOT_TOKEN") or ""
    
    # Adminlar ID lari
    ADMIN_IDS_RAW: str = os.getenv("ADMIN_ID") or os.getenv("ADMIN_IDS") or ""
    
    # Kanal ID si
    CHANNEL_ID_RAW: str = os.getenv("CANAL_ID") or os.getenv("CHANNEL_ID") or ""
    
    # Rasm va boshqa media
    IMAGE_URL: str = os.getenv("IMAGE_URL", "")
    IMAGE_CAPTION: str = os.getenv("IMAGE_CAPTION", "")

    # PostgreSQL sozlamalari (moslashuvchan nomlar)
    DB_HOST: str = os.getenv("PGHOST") or os.getenv("HOST") or os.getenv("DB_HOST") or "localhost"
    DB_PORT: int = int(os.getenv("PGPORT") or os.getenv("PORT") or os.getenv("DB_PORT") or 5432)
    DB_USER: str = os.getenv("PGUSER") or os.getenv("USER") or os.getenv("DB_USER") or "postgres"
    DB_PASSWORD: str = os.getenv("PGPASSWORD") or os.getenv("PASSWORD") or os.getenv("DB_PASSWORD") or "123456"
    DB_NAME: str = os.getenv("PGDATABASE") or os.getenv("DATABASE") or os.getenv("DB_NAME") or "webcervice"

    @property
    def admin_ids(self) -> List[int]:
        """Admin ID larini xavfsiz int list ko'rinishida olish"""
        if not self.ADMIN_IDS_RAW:
            return []
        ids = []
        for part in self.ADMIN_IDS_RAW.split(","):
            part = part.strip()
            if part.isdigit() or (part.startswith("-") and part[1:].isdigit()):
                ids.append(int(part))
        return ids

    @property
    def channel_id(self):
        """Kanal ID sini olish (int yoki string)"""
        if not self.CHANNEL_ID_RAW:
            return None
        val = self.CHANNEL_ID_RAW.strip()
        try:
            return int(val)
        except ValueError:
            return val

settings = Settings()
