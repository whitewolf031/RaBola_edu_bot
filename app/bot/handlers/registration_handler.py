import re
from telebot import types
from app.bot.bot_instance import bot
from app.services.user_service import user_service
from app.services.lead_service import lead_service
from app.bot.keyboards.reply import main_menu, phone_request_menu, back_menu
from app.bot.keyboards.inline import confirm_registration_markup
from app.locales.keyboard_texts import register, back
from app.locales.texts import (
    your_name, your_number, name, number, sent_to_admin, choose_section, get_msg
)
from app.bot.state import state_manager, States
from app.core.logger import logger

def clean_and_validate_phone(raw_phone: str) -> tuple[bool, str]:
    """Telefon raqamni tozalash va tekshirish"""
    # Raqamlarni ajratib olish
    digits = re.sub(r"\D", "", raw_phone)
    
    # 998 bilan boshlanishi yoki 9 ta raqam bo'lsa 998 qo'shish
    if len(digits) == 9:
        digits = "998" + digits
    elif len(digits) == 12 and digits.startswith("998"):
        pass
    else:
        # Boshqa davlat raqamlari bo'lsa (10-15 xonali)
        if 10 <= len(digits) <= 15:
            return True, f"+{digits}"
        return False, raw_phone

    # O'zbekiston raqami tekshiruvi: 998 + 9 xona
    if len(digits) == 12 and digits.startswith("998"):
        return True, f"+{digits}"
    
    return False, raw_phone

def register_registration_handlers():
    register_values = list(register.values())

    # 1. Ro'yxatdan o'tish tugmasi bosilganda
    @bot.message_handler(chat_types=['private'], func=lambda msg: msg.text in register_values)
    def handle_registration_start(message: types.Message):
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)
        state_manager.set_state(chat_id, States.WAITING_NAME)
        prompt = your_name.get(lang, "To'liq ism-familiyangizni kiriting:")
        bot.send_message(chat_id, prompt, reply_markup=back_menu(lang))

    # 2. Ism kiritish holati
    @bot.message_handler(chat_types=['private'], func=lambda msg: state_manager.get_state(msg.chat.id) == States.WAITING_NAME)
    def handle_name_input(message: types.Message):
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)

        # Agar orqaga bosilgan bo'lsa
        if message.text in list(back.values()):
            state_manager.clear(chat_id)
            bot.send_message(chat_id, choose_section.get(lang, "Asosiy menyu"), reply_markup=main_menu(lang))
            return

        fio = message.text.strip()
        if len(fio) < 2:
            bot.send_message(chat_id, "Iltimos, to'liq ismingizni kiriting:")
            return

        state_manager.set_data(chat_id, "fio", fio)
        state_manager.set_state(chat_id, States.WAITING_PHONE)

        phone_prompt = your_number.get(lang, "Telefon raqamingizni yuboring:")
        bot.send_message(chat_id, phone_prompt, reply_markup=phone_request_menu(lang))

    # 3. Telefon kiritish holati (matn yoki kontakt)
    @bot.message_handler(
        chat_types=['private'],
        func=lambda msg: state_manager.get_state(msg.chat.id) == States.WAITING_PHONE,
        content_types=["text", "contact"]
    )
    def handle_phone_input(message: types.Message):
        chat_id = message.chat.id
        lang = user_service.get_language(chat_id)

        # Agar orqaga bosilgan bo'lsa
        if message.text and message.text in list(back.values()):
            state_manager.clear(chat_id)
            bot.send_message(chat_id, choose_section.get(lang, "Asosiy menyu"), reply_markup=main_menu(lang))
            return

        raw_phone = ""
        if message.contact:
            raw_phone = message.contact.phone_number
        elif message.text:
            raw_phone = message.text

        is_valid, formatted_phone = clean_and_validate_phone(raw_phone)
        if not is_valid:
            bot.send_message(chat_id, get_msg("invalid_phone", lang), reply_markup=phone_request_menu(lang))
            return

        state_manager.set_data(chat_id, "phone", formatted_phone)
        fio = state_manager.get_data(chat_id, "fio") or "Noma'lum"

        name_lbl = name.get(lang, "Ism:")
        num_lbl = number.get(lang, "Telefon:")
        confirm_text = f"{name_lbl} {fio}\n{num_lbl} {formatted_phone}"

        bot.send_message(chat_id, confirm_text, reply_markup=confirm_registration_markup(lang))

    # 4. Inline tasdiqlash / bekor qilish
    @bot.callback_query_handler(func=lambda call: call.data in ["reg:confirm", "reg:cancel", "yes", "no"])
    def handle_registration_callback(call: types.CallbackQuery):
        if call.message.chat.type != 'private':
            return
        chat_id = call.message.chat.id
        lang = user_service.get_language(chat_id)
        data = call.data

        fio = state_manager.get_data(chat_id, "fio")
        phone = state_manager.get_data(chat_id, "phone")
        course = state_manager.get_data(chat_id, "course") or ""

        # Eski inline "yes"/"no" larni ham qo'llab-quvvatlash
        if data in ["reg:confirm", "yes"]:
            if fio and phone:
                # DB ga va kanalga xavfsiz yuborish
                lead_service.process_application(
                    bot=bot,
                    chat_id=chat_id,
                    full_name=fio,
                    phone_number=phone,
                    course_name=course,
                    lang=lang
                )
                success_text = sent_to_admin.get(lang, get_msg("success_lead", lang))
                bot.send_message(chat_id, success_text)
            else:
                # Agar ma'lumot xotiradan o'chib ketgan bo'lsa
                bot.send_message(chat_id, get_msg("canceled", lang))

            state_manager.clear(chat_id)
            bot.send_message(chat_id, choose_section.get(lang, "Asosiy menyu"), reply_markup=main_menu(lang))

        elif data in ["reg:cancel", "no"]:
            state_manager.clear(chat_id)
            bot.send_message(chat_id, get_msg("canceled", lang))
            bot.send_message(chat_id, choose_section.get(lang, "Asosiy menyu"), reply_markup=main_menu(lang))

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
