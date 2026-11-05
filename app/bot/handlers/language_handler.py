from telebot import types
from app.bot.bot_instance import bot
from app.services.user_service import user_service
from app.bot.keyboards.inline import language_inline_markup
from app.bot.keyboards.reply import main_menu
from app.locales.texts import choose_section, get_msg
from app.locales.keyboard_texts import change_languange
from app.core.logger import logger

def register_language_handlers():
    # 1. Inline tugma orqali til tanlanganda
    @bot.callback_query_handler(func=lambda call: call.data.startswith("lang:") or call.data in ["uz", "ru", "en"])
    def handle_language_selection(call: types.CallbackQuery):
        if call.message.chat.type != 'private':
            return
        chat_id = call.message.chat.id
        raw_data = call.data
        if raw_data.startswith("lang:"):
            lang = raw_data.split(":", 1)[1]
        else:
            lang = raw_data

        if lang not in ["uz", "ru", "en"]:
            lang = "uz"

        # BAZADA SAQLASH (Foydalanuvchi talabi!)
        user_service.set_language(chat_id, lang)

        # Eski inline xabarga javob berish
        try:
            bot.answer_callback_query(call.id, text=get_msg("lang_changed", lang))
        except Exception:
            pass

        section_text = choose_section.get(lang, "Bo'limlardan birini tanlang:")
        bot.send_message(chat_id, section_text, reply_markup=main_menu(lang))
        logger.info(f"Foydalanuvchi {chat_id} tilini '{lang}' ga o'zgartirdi va DB da saqlandi.")

    # 2. Reply menyudan "Tilni o'zgartirish 🔄" bosilganda
    change_lang_values = list(change_languange.values())

    @bot.message_handler(chat_types=['private'], func=lambda msg: msg.text in change_lang_values or (msg.text and "til" in msg.text.lower() and "o'zgartirish" in msg.text.lower()))
    def handle_change_language_button(message: types.Message):
        chat_id = message.chat.id
        bot.send_message(
            chat_id,
            "Tilni tanlang / Выберите язык / Choose language:",
            reply_markup=language_inline_markup()
        )
