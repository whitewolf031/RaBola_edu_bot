from telebot import types
from app.locales.keyboard_texts import (
    aboutcourse, connect, register, aboutus, taklif_button, change_languange,
    back, computer_literacy, office_management, foundation, accounting,
    robotics, digital_kids, devops_engineering, full_steck, share_phone_number
)

def main_menu(lang: str = "uz") -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(aboutcourse.get(lang, "Kurslar haqida 📚"))
    btn2 = types.KeyboardButton(connect.get(lang, "Biz bilan bog'laning📞"))
    btn3 = types.KeyboardButton(register.get(lang, "Ro'yxatdan o'tish📄"))
    btn4 = types.KeyboardButton(aboutus.get(lang, "Biz haqimizda 📖"))
    btn5 = types.KeyboardButton(taklif_button.get(lang, "Bizning taklifimiz📝"))
    btn6 = types.KeyboardButton(change_languange.get(lang, "Tilni o'zgartirish 🔄"))
    
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    markup.row(btn6)
    return markup

def courses_menu(lang: str = "uz") -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(computer_literacy.get(lang, "Kampyuter savodxonligi👩‍💻"))
    btn2 = types.KeyboardButton(office_management.get(lang, "Ofis menejerligi🖋️"))
    btn3 = types.KeyboardButton(foundation.get(lang, "Dasturlash asoslari👨‍💻"))
    btn4 = types.KeyboardButton(accounting.get(lang, "Buxgalteriya 1C"))
    btn5 = types.KeyboardButton(robotics.get(lang, "Robototexnika🤖"))
    btn6 = types.KeyboardButton(digital_kids.get(lang, "Raqamli bolalar"))
    btn7 = types.KeyboardButton(devops_engineering.get(lang, "DevOps muhandisligi"))
    btn8 = types.KeyboardButton(full_steck.get(lang, "Full Stack dasturchi"))
    btn_back = types.KeyboardButton(back.get(lang, "Orqaga🔙"))
    
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    markup.row(btn7, btn8)
    markup.row(btn_back)
    return markup

def course_detail_menu(lang: str = "uz") -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_reg = types.KeyboardButton(register.get(lang, "Ro'yxatdan o'tish📄"))
    btn_back = types.KeyboardButton(back.get(lang, "Orqaga🔙"))
    markup.row(btn_reg)
    markup.row(btn_back)
    return markup

def phone_request_menu(lang: str = "uz") -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_phone = types.KeyboardButton(share_phone_number.get(lang, "Telefon raqamni yuborish📲"), request_contact=True)
    btn_back = types.KeyboardButton(back.get(lang, "Orqaga🔙"))
    markup.row(btn_phone)
    markup.row(btn_back)
    return markup

def back_menu(lang: str = "uz") -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton(back.get(lang, "Orqaga🔙"))
    markup.row(btn_back)
    return markup

def admin_menu() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Yangilik qo'shish")
    btn2 = types.KeyboardButton("📊 Statistika")
    btn3 = types.KeyboardButton("🏠 Bosh menyu")
    markup.row(btn1, btn2)
    markup.row(btn3)
    return markup
