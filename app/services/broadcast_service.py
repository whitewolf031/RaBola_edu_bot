import time
from typing import Optional
from app.services.user_service import user_service
from app.core.logger import logger

class BroadcastService:
    def send_broadcast(self, bot, content_type: str, text: Optional[str] = None, photo_id: Optional[str] = None, caption: Optional[str] = None) -> tuple:
        """Barcha foydalanuvchilarga xabar tarqatish (flood control bilan)"""
        users = user_service.get_all_users()
        success = 0
        failed = 0

        logger.info(f"Broadcast boshlanmoqda: {len(users)} ta foydalanuvchiga...")

        for index, user_id in enumerate(users):
            try:
                if content_type == "photo" and photo_id:
                    bot.send_photo(user_id, photo_id, caption=caption)
                elif content_type == "text" and text:
                    bot.send_message(user_id, text)
                success += 1
            except Exception as e:
                failed += 1
                logger.warning(f"Broadcast xatosi ({user_id}): {e}")

            # Telegram rate limit (sekundiga 30 ta xabar): har 25 ta xabardan so'ng 1s kutish
            if index > 0 and index % 25 == 0:
                time.sleep(1)

        logger.info(f"Broadcast yakunlandi. Muvaffaqiyatli: {success}, Xatoliklar: {failed}")
        return success, failed

broadcast_service = BroadcastService()
