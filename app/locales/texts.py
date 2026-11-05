import sys
import os

# Localisation papkasidagi barcha matnlarni import qilamiz
try:
    from Localisation.lang import *
    from Localisation.keyboard_lang import *
except ImportError:
    pass

# Qo'shimcha tizimli matnlar
system_messages = {
    "uz": {
        "welcome": "Assalomu alaykum! Xush kelibsiz. Tilni tanlang:",
        "lang_changed": "Til muvaffaqiyatli o'zgartirildi! ✅",
        "invalid_phone": "Telefon raqam noto‘g‘ri formatda! ❌\nIltimos, qayta kiriting (Masalan: +998901234567 yoki pastdagi tugmani bosing):",
        "enter_phone": "Telefon raqamingizni yuboring 📱:",
        "confirm_prompt": "Ma'lumotlaringiz to'g'rimi?\n\n👤 Ism: {fio}\n📞 Telefon: {phone}",
        "success_lead": "Arizangiz muvaffaqiyatli qabul qilindi! Tez orada mutaxassislarimiz siz bilan bog'lanishadi. ✅",
        "canceled": "Amal bekor qilindi.",
        "unknown_cmd": "Noma'lum buyruq. Iltimos, menyudan foydalaning.",
        "admin_welcome": "🛠 Admin panelga xush kelibsiz!",
        "admin_stats": "📊 Statistika:\n👥 Jami foydalanuvchilar: {users_count}\n📝 Jami arizalar: {apps_count}",
        "admin_send_news": "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabarni (matn yoki rasm) yuboring:",
        "broadcast_started": "📢 Xabar barcha foydalanuvchilarga yuborilmoqda...",
        "broadcast_finished": "✅ Xabar yuborish yakunlandi!\nYetib bordi: {success} ta\nXato/Bloklangan: {failed} ta",
    },
    "ru": {
        "welcome": "Здравствуйте! Добро пожаловать. Выберите язык:",
        "lang_changed": "Язык успешно изменен! ✅",
        "invalid_phone": "Номер телефона введен неверно! ❌\nПожалуйста, введите заново (Например: +998901234567 или используйте кнопку ниже):",
        "enter_phone": "Отправьте ваш номер телефона 📱:",
        "confirm_prompt": "Ваши данные верны?\n\n👤 Имя: {fio}\n📞 Телефон: {phone}",
        "success_lead": "Ваша заявка успешно принята! Наши специалисты свяжутся с вами в ближайшее время. ✅",
        "canceled": "Действие отменено.",
        "unknown_cmd": "Неизвестная команда. Пожалуйста, используйте меню.",
        "admin_welcome": "🛠 Добро пожаловать в панель администратора!",
        "admin_stats": "📊 Статистика:\n👥 Всего пользователей: {users_count}\n📝 Всего заявок: {apps_count}",
        "admin_send_news": "Отправьте сообщение (текст или фото) для рассылки всем пользователям:",
        "broadcast_started": "📢 Сообщение рассылается всем пользователям...",
        "broadcast_finished": "✅ Рассылка завершена!\nДоставлено: {success}\nОшибок/Блокировок: {failed}",
    },
    "en": {
        "welcome": "Hello! Welcome. Please select a language:",
        "lang_changed": "Language successfully changed! ✅",
        "invalid_phone": "Invalid phone number format! ❌\nPlease enter again (e.g. +998901234567 or use the button below):",
        "enter_phone": "Please send your phone number 📱:",
        "confirm_prompt": "Are your details correct?\n\n👤 Name: {fio}\n📞 Phone: {phone}",
        "success_lead": "Your application has been received! We will contact you soon. ✅",
        "canceled": "Action cancelled.",
        "unknown_cmd": "Unknown command. Please use the menu.",
        "admin_welcome": "🛠 Welcome to the Admin Panel!",
        "admin_stats": "📊 Statistics:\n👥 Total users: {users_count}\n📝 Total applications: {apps_count}",
        "admin_send_news": "Send the announcement (text or photo) to broadcast to all users:",
        "broadcast_started": "📢 Broadcasting message to all users...",
        "broadcast_finished": "✅ Broadcast completed!\nDelivered: {success}\nFailed/Blocked: {failed}",
    }
}

def get_msg(key: str, lang: str = "uz", **kwargs) -> str:
    lang = lang if lang in ["uz", "ru", "en"] else "uz"
    msg = system_messages.get(lang, {}).get(key, system_messages["uz"].get(key, ""))
    if kwargs:
        return msg.format(**kwargs)
    return msg
