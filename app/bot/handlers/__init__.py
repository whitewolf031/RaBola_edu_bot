from telebot import types
from app.bot.bot_instance import bot
from app.bot.handlers.start_handler import register_start_handlers
from app.bot.handlers.language_handler import register_language_handlers
from app.bot.handlers.admin_handler import register_admin_handlers
from app.bot.handlers.registration_handler import register_registration_handlers
from app.bot.handlers.course_handler import register_course_handlers
from app.bot.handlers.menu_handler import register_menu_handlers
from app.services.user_service import user_service
from app.bot.keyboards.reply import main_menu
from app.locales.texts import choose_section

def register_all_handlers():
    """Barcha bot handlerlarini to'g'ri tartibda ro'yxatdan o'tkazish"""
    register_start_handlers()
    register_language_handlers()
    register_admin_handlers()
    register_registration_handlers()
    register_course_handlers()
    register_menu_handlers()

    # Fallback handler: Agar hech bir handlerga tushmagan noma'lum matn kelsa
    @bot.message_handler(chat_types=['private'], func=lambda msg: True, content_types=['text'])
    def fallback_handler(message: types.Message):
        if message.chat.type != 'private':
            return
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)
        # Foydalanuvchiga asosiy menyuni chiqarib yordam beramiz
        bot.send_message(
            chat_id,
            choose_section.get(lang, "Iltimos, quyidagi menyudan foydalaning:"),
            reply_markup=main_menu(lang)
        )
