from app.database.repositories.app_repo import app_repo
from app.core.config import settings
from app.core.logger import logger
from app.locales.texts import new_student, ismi, tel

class LeadService:
    def process_application(self, bot, chat_id: int, full_name: str, phone_number: str, course_name: str = "", lang: str = "uz"):
        """Arizani qabul qilish, bazaga saqlash va kanalga yuborish"""
        # 1. Bazaga saqlash
        try:
            app_repo.add_application(
                chat_id=chat_id,
                full_name=full_name,
                phone_number=phone_number,
                course_name=course_name
            )
        except Exception as e:
            logger.error(f"Arizani DB ga saqlashda xatolik: {e}")

        # 2. Kanalga xabar yuborish
        channel_id = settings.channel_id
        if channel_id:
            try:
                # Yangi o'quvchi xabari
                ns = new_student.get(lang, "🆕 Yangi o'quvchi!\n")
                ism = ismi.get(lang, "👤 Ismi: ")
                t = tel.get(lang, "📞 Tel: ")

                channel_msg = f"{ns}{ism}{full_name}\n{t}{phone_number}"
                if course_name:
                    channel_msg += f"\n📚 Kurs: {course_name}"
                
                bot.send_message(channel_id, channel_msg)
                logger.info(f"Yangi ariza kanalga ({channel_id}) muvaffaqiyatli yuborildi.")
            except Exception as e:
                logger.error(f"Kanalga ({channel_id}) xabar yuborishda xatolik: {e}")
        else:
            logger.warning("CANAL_ID sozlanmagan, kanalga ariza yuborilmadi.")

    def get_applications_count(self) -> int:
        return app_repo.get_applications_count()

lead_service = LeadService()
