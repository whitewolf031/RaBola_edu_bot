import telebot
from telebot import custom_filters
from telebot.handler_backends import CancelUpdate
from app.core.config import settings
from app.core.logger import logger

# Middleware tizimini yoqish
telebot.apihelper.ENABLE_MIDDLEWARE = True

token = settings.BOT_TOKEN
if not token:
    logger.warning("BOT_TOKEN aniqlanmadi! .env faylni tekshiring.")
    token = "0000000000:DEFAULT_DUMMY_TOKEN_PLEASE_SET_ENV"

# threaded=False resurslarni kam sarflaydi, thread limitlariga uchramaydi va eng barqaror ishlaydi
bot = telebot.TeleBot(token=token, threaded=False, parse_mode=None)

# ChatFilter ni qo'shish (chat_types=['private'] ni qo'llab-quvvatlash uchun)
bot.add_custom_filter(custom_filters.ChatFilter())

# 1-darajali himoya: Middleware orqali guruh va kanallardagi barcha yangilanishlarni to'xtatish
@bot.middleware_handler(update_types=['message', 'callback_query'])
def enforce_private_chats_only(bot_instance, update):
    """
    Bot guruhlar va kanallarda hech qanday xabarga javob bermasligi,
    faqat shaxsiy chatda (lichkada) ishlashi uchun middleware filtri.
    """
    chat = getattr(update, 'chat', None)
    if not chat:
        message = getattr(update, 'message', None)
        chat = getattr(message, 'chat', None)

    if chat and chat.type != 'private':
        return CancelUpdate()
