from telebot import types
from app.bot.bot_instance import bot
from app.core.config import settings
from app.services.user_service import user_service
from app.services.lead_service import lead_service
from app.services.broadcast_service import broadcast_service
from app.bot.keyboards.reply import admin_menu, main_menu
from app.bot.state import state_manager, States
from app.locales.texts import get_msg
from app.core.logger import logger

def is_admin(chat_id: int) -> bool:
    return chat_id in settings.admin_ids

def register_admin_handlers():
    # 1. /admin buyrug'i
    @bot.message_handler(commands=['admin'], chat_types=['private'])
    def handle_admin_command(message: types.Message):
        chat_id = message.chat.id
        if not is_admin(chat_id):
            bot.send_message(chat_id, "⛔ Kechirasiz, siz admin emassiz!")
            return

        state_manager.clear(chat_id)
        bot.send_message(chat_id, "🛠 Admin panelga xush kelibsiz!", reply_markup=admin_menu())

    # 2. Statistika
    @bot.message_handler(chat_types=['private'], func=lambda msg: is_admin(msg.chat.id) and msg.text == "📊 Statistika")
    def handle_admin_stats(message: types.Message):
        chat_id = message.chat.id
        users_count = user_service.get_users_count()
        apps_count = lead_service.get_applications_count()

        stats_text = (
            f"📊 <b>Bot Statistikasi:</b>\n\n"
            f"👥 Jami foydalanuvchilar: <b>{users_count}</b> ta\n"
            f"📝 Jami arizalar: <b>{apps_count}</b> ta\n"
        )
        bot.send_message(chat_id, stats_text, parse_mode="HTML", reply_markup=admin_menu())

    # 3. Yangilik qo'shish bosilganda
    @bot.message_handler(chat_types=['private'], func=lambda msg: is_admin(msg.chat.id) and msg.text == "Yangilik qo'shish")
    def handle_start_broadcast(message: types.Message):
        chat_id = message.chat.id
        state_manager.set_state(chat_id, States.ADMIN_WAITING_ANNOUNCEMENT)
        bot.send_message(
            chat_id,
            "📢 Barcha foydalanuvchilarga yubormoqchi bo'lgan yangilikni yuboring (Matn yoki Rasm):",
            reply_markup=admin_menu()
        )

    # 4. Yangilikni qabul qilish va tarqatish
    @bot.message_handler(
        chat_types=['private'],
        func=lambda msg: is_admin(msg.chat.id) and state_manager.get_state(msg.chat.id) == States.ADMIN_WAITING_ANNOUNCEMENT,
        content_types=["text", "photo"]
    )
    def handle_broadcast_message(message: types.Message):
        chat_id = message.chat.id

        # Agar admin bekor qilmoqchi bo'lsa
        if message.text in ["🏠 Bosh menyu", "📊 Statistika"]:
            state_manager.clear(chat_id)
            if message.text == "🏠 Bosh menyu":
                lang = user_service.get_language(chat_id)
                bot.send_message(chat_id, "Asosiy menyu", reply_markup=main_menu(lang))
            return

        bot.send_message(chat_id, "📢 Xabar barcha foydalanuvchilarga yuborilmoqda, kuting...")

        success = 0
        failed = 0

        if message.content_type == "photo":
            photo_id = message.photo[-1].file_id
            caption = message.caption or ""
            success, failed = broadcast_service.send_broadcast(
                bot=bot,
                content_type="photo",
                photo_id=photo_id,
                caption=caption
            )
        elif message.content_type == "text":
            success, failed = broadcast_service.send_broadcast(
                bot=bot,
                content_type="text",
                text=message.text
            )

        state_manager.clear(chat_id)
        report = (
            f"✅ <b>Yangilik muvaffaqiyatli tarqatildi!</b>\n\n"
            f"📨 Yetkazildi: {success} ta\n"
            f"❌ Yetkazilmadi (bloklaganlar): {failed} ta"
        )
        bot.send_message(chat_id, report, parse_mode="HTML", reply_markup=admin_menu())
