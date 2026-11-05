from telebot import types
from app.bot.bot_instance import bot
from app.services.user_service import user_service
from app.bot.keyboards.inline import language_inline_markup
from app.bot.keyboards.reply import main_menu
from app.locales.texts import choose_section, get_msg
from app.bot.state import state_manager
from app.core.logger import logger

def register_start_handlers():
    @bot.message_handler(commands=['start'], chat_types=['private'])
    def handle_start(message: types.Message):
        if message.chat.type != 'private':
            return
        chat_id = message.chat.id
        username = message.from_user.username
        full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()

        # State ni tozalash
        state_manager.clear(chat_id)

        # Foydalanuvchini bazada qayd etish
        user_service.register_user(chat_id=chat_id, username=username, full_name=full_name)

        # Tilni tekshirish
        current_lang = user_service.get_language(chat_id)
        
        # Har safar /start bosganda yoki birinchi marta tilni tanlashni taklif qilish
        welcome_text = (
            "Assalomu alaykum! iTechAcademy (RaBola) botiga xush kelibsiz.\n"
            "Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please choose language:"
        )
        bot.send_message(chat_id, welcome_text, reply_markup=language_inline_markup())
        logger.info(f"Foydalanuvchi {chat_id} /start bosdi.")

    @bot.message_handler(commands=['help'], chat_types=['private'])
    def handle_help(message: types.Message):
        if message.chat.type != 'private':
            return
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)
        bot.send_message(
            chat_id,
            "Bot orqali kurslarimiz bilan tanishishingiz va o'qishga ro'yxatdan o'tishingiz mumkin.",
            reply_markup=main_menu(lang)
        )
