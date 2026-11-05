from telebot import types
from app.bot.bot_instance import bot
from app.services.user_service import user_service
from app.bot.keyboards.reply import main_menu, courses_menu, back_menu
from app.locales.keyboard_texts import (
    aboutcourse, connect, aboutus, taklif_button, back
)
from app.locales.texts import (
    course_choose, contact_with_us, info, our_offer_lang, choose_section
)
from app.bot.state import state_manager

def register_menu_handlers():
    aboutcourse_values = list(aboutcourse.values())
    connect_values = list(connect.values())
    aboutus_values = list(aboutus.values())
    taklif_values = list(taklif_button.values())
    back_values = list(back.values()) + ["🏠 Bosh menyu"]

    # 1. Kurslar haqida
    @bot.message_handler(chat_types=['private'], func=lambda msg: msg.text in aboutcourse_values)
    def handle_about_courses(message: types.Message):
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)
        state_manager.clear(chat_id)
        text = course_choose.get(lang, "Kurslarimizni tanlang")
        bot.send_message(chat_id, text, reply_markup=courses_menu(lang), parse_mode="HTML")

    # 2. Biz bilan bog'laning
    @bot.message_handler(chat_types=['private'], func=lambda msg: msg.text in connect_values)
    def handle_connect(message: types.Message):
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)
        state_manager.clear(chat_id)
        text = contact_with_us.get(lang, "")
        bot.send_message(chat_id, text, reply_markup=back_menu(lang), parse_mode="HTML")

    # 3. Biz haqimizda
    @bot.message_handler(chat_types=['private'], func=lambda msg: msg.text in aboutus_values)
    def handle_about_us(message: types.Message):
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)
        state_manager.clear(chat_id)
        text = info.get(lang, "")
        bot.send_message(chat_id, text, reply_markup=back_menu(lang), parse_mode="HTML")

    # 4. Bizning taklifimiz
    @bot.message_handler(chat_types=['private'], func=lambda msg: msg.text in taklif_values)
    def handle_our_offer(message: types.Message):
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)
        state_manager.clear(chat_id)
        text = our_offer_lang.get(lang, "")
        bot.send_message(chat_id, text, reply_markup=back_menu(lang), parse_mode="HTML")

    # 5. Orqaga
    @bot.message_handler(chat_types=['private'], func=lambda msg: msg.text in back_values)
    def handle_back(message: types.Message):
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)
        state_manager.clear(chat_id)
        text = choose_section.get(lang, "Bo'limlardan birini tanlang:")
        bot.send_message(chat_id, text, reply_markup=main_menu(lang))
