import time
import threading
from datetime import datetime
import schedule
from app.core.config import settings
from app.core.logger import logger

class SchedulerService:
    def __init__(self, bot=None):
        self.bot = bot
        self._thread = None
        self._running = False

    def set_bot(self, bot):
        self.bot = bot

    def send_status_update(self):
        if not self.bot:
            return
        channel_id = settings.channel_id
        if not channel_id:
            logger.info("Scheduler: CANAL_ID belgilanmagan, status xabari o'tkazib yuborildi.")
            return

        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"*iTechAcademy* Bot is working.\n*Date & Time*: {current_time}"
            self.bot.send_message(channel_id, message, parse_mode="Markdown")
            logger.info(f"Kanalga ({channel_id}) status yangilanishi yuborildi.")
        except Exception as e:
            logger.warning(f"Scheduler: Kanalga ({channel_id}) status yuborishda xatolik: {e}")

    def _run_schedule(self):
        while self._running:
            try:
                schedule.run_pending()
            except Exception as e:
                logger.error(f"Scheduler ishida xatolik: {e}")
            time.sleep(1)

    def start(self):
        if self._running:
            return
        self._running = True
        
        # Har kuni 20:00 da yuborish
        schedule.every().day.at("20:00").do(self.send_status_update)
        
        # Dastlabki tekshirishni xavfsiz bajarish (kechiktirilgan 5 soniyadan so'ng)
        threading.Timer(5.0, self.send_status_update).start()

        self._thread = threading.Thread(target=self._run_schedule, daemon=True)
        self._thread.start()
        logger.info("Scheduler fon xizmati ishga tushdi.")

scheduler_service = SchedulerService()
