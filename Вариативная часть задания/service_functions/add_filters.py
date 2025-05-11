from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import StateFilter

# --------------------------------------------- Добавление фильтров ------------------------------------
def add_filters(bot: AsyncTeleBot):
    bot.add_custom_filter(StateFilter(bot)) # фильтр с состояниями
# ----------------------------------------------------------------------------------------------------