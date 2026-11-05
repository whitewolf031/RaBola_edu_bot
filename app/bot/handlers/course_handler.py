from telebot import types
from app.bot.bot_instance import bot
from app.services.user_service import user_service
from app.bot.keyboards.reply import course_detail_menu
from app.locales.keyboard_texts import (
    computer_literacy, office_management, foundation, accounting,
    robotics, digital_kids, devops_engineering, full_steck
)
from app.locales.texts import (
    info_computer_literacy, office_menegerlik, info_foundation,
    info_accounting, info_robotics, info_digital_kids,
    info_devops_engineering, info_fullstack_development
)
from app.bot.state import state_manager

def register_course_handlers():
    courses_map = [
        (computer_literacy, info_computer_literacy, "Kompyuter savodxonligi"),
        (office_management, office_menegerlik, "Ofis menejerligi"),
        (foundation, info_foundation, "Dasturlash asoslari"),
        (accounting, info_accounting, "Buxgalteriya 1C"),
        (robotics, info_robotics, "Robototexnika"),
        (digital_kids, info_digital_kids, "Raqamli bolalar"),
        (devops_engineering, info_devops_engineering, "DevOps muhandisligi"),
        (full_steck, info_fullstack_development, "Full Stack dasturchi"),
    ]

    for btn_dict, info_dict, course_name in courses_map:
        btn_texts = list(btn_dict.values())

        def make_handler(b_texts=btn_texts, i_dict=info_dict, c_name=course_name):
            @bot.message_handler(chat_types=['private'], func=lambda msg: msg.text in b_texts)
            def handle_course(message: types.Message):
                chat_id = message.chat.id
                lang = user_service.get_language(chat_id)
                # Kurs nomini state ga saqlab qo'yamiz
                state_manager.set_data(chat_id, "course", c_name)
                detail_text = i_dict.get(lang, "")
                bot.send_message(chat_id, detail_text, reply_markup=course_detail_menu(lang), parse_mode="HTML")
            return handle_course

        make_handler()
