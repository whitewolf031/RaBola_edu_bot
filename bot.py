import time
import sys
from app.core.config import settings
from app.core.logger import logger
from app.database.migrations import run_migrations
from app.bot.bot_instance import bot
from app.bot.handlers import register_all_handlers
from app.services.scheduler_service import scheduler_service

def main():
    logger.info("==========================================")
    logger.info("iTechAcademy (RaBola) Bot ishga tushmoqda...")
    logger.info("==========================================")

    # 1. Ma'lumotlar bazasi migratsiyalarini bajarish
    try:
        run_migrations()
    except Exception as e:
        logger.error(f"Migratsiyalarni bajarishda xatolik: {e}")

    # 2. Bot handlerlarini ro'yxatdan o'tkazish
    register_all_handlers()
    logger.info("Bot handlerlari muvaffaqiyatli ro'yxatdan o'tkazildi.")

    # 3. Scheduler xizmatini ishga tushirish
    scheduler_service.set_bot(bot)
    try:
        scheduler_service.start()
    except Exception as e:
        logger.error(f"Scheduler xizmatini boshlashda xatolik: {e}")

    # 4. Supervised Polling Loop (Serverda bot o'chib qolishining oldini oladi)
    logger.info("Bot Telegram serveriga ulanmoqda (Infinity Polling)...")
    retry_delay = 5

    while True:
        try:
            bot.infinity_polling(
                timeout=60,
                long_polling_timeout=30,
                skip_pending=False
            )
        except KeyboardInterrupt:
            logger.info("Bot foydalanuvchi tomonidan to'xtatildi (Ctrl+C).")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Telegram pollingda kutilmagan xatolik yuz berdi: {e}")
            logger.info(f"{retry_delay} soniyadan so'ng avtomatik qayta ulanadi...")
            time.sleep(retry_delay)

if __name__ == "__main__":
    main()