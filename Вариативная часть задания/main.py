import os # для виртуальных переменных
from dotenv import load_dotenv # для поиска файла с виртуальными переменными
from telebot.async_telebot import AsyncTeleBot # объект асинхронного бота
from service_functions.add_filters import add_filters # функция для добавления фильтров в бота
import asyncio # библиотека для асинхронности
import logging # библиотека для логирования
from handlers.handlers import * # импортируем все обработчики

# ------------------------------------------------СЛУЖЕБНЫЕ ПЕРЕМЕННЫЕ -----------------------------
logging.basicConfig(level=logging.DEBUG)  # логирование
load_dotenv('./.env') # загружаем переменные из виртуального окружения в систему
BOT_TOKEN: str = os.getenv('tg_bot_token')
Bot: AsyncTeleBot = AsyncTeleBot(token=BOT_TOKEN, parse_mode='HTML')
# --------------------------------------------------------------------------------------------------


# -----------------------------------------------Точка входа----------------------------------------
async def main(): # запускаем бота
    add_filters(Bot) # добавляем фильтры в бота. Для добавления новых фильтров нужно отредактировать эту функцию

    # --------------регистрация хендлеров--------------
    handler_start(Bot)
    handler_get_weather_by_location(Bot)
    handler_check_weather_in_city(Bot)
    handler_get_weather_by_city(Bot)
    handler_stop_trying_inline_button(Bot)
    Bot.add_callback_query_handler(Bot)
    # --------------------------------------------------

    await Bot.polling(skip_pending=True) # запускаем цикл запросов на сервера Telegram
# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    asyncio.run(main()) # запускаем main
