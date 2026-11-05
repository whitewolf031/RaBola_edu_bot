from telebot import types
from app.locales.texts import yes_lang, no_lang

def language_inline_markup() -> types.InlineKeyboardMarkup:
    """Tilni tanlash uchun inline tugmalar"""
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_uz = types.InlineKeyboardButton(text="🇺🇿 Uz", callback_data="lang:uz")
    btn_ru = types.InlineKeyboardButton(text="🇷🇺 Ru", callback_data="lang:ru")
    btn_en = types.InlineKeyboardButton(text="🇺🇸 En", callback_data="lang:en")
    markup.row(btn_uz, btn_ru, btn_en)
    return markup

def confirm_registration_markup(lang: str = "uz") -> types.InlineKeyboardMarkup:
    """Ro'yxatdan o'tishni tasdiqlash uchun inline tugmalar"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    yes_text = yes_lang.get(lang, "yes")
    no_text = no_lang.get(lang, "no")
    
    # Chiroyli ko'rinish
    yes_label = "✅ Ha" if lang == "uz" else ("✅ Да" if lang == "ru" else "✅ Yes")
    no_label = "❌ Yo'q" if lang == "uz" else ("❌ Нет" if lang == "ru" else "❌ No")

    btn_yes = types.InlineKeyboardButton(text=yes_label, callback_data="reg:confirm")
    btn_no = types.InlineKeyboardButton(text=no_label, callback_data="reg:cancel")
    markup.row(btn_yes, btn_no)
    return markup
