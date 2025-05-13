import asyncio

from telebot.async_telebot import AsyncTeleBot # импортируем класс асинхронного бота
import service_functions.api_weather as api_weather # импорт апи для получения погоды
from telebot.types import Message, CallbackQuery # импорт класса сообщения в телеграмм
import service_functions.keyboard as keyboard # импортируем наши клавиатуры
from service_functions.states import States # импорт наших состояний FSM
from  service_functions.custom_error import * # импорт кастомного класса ошибок.
from service_functions.states import States # импорт класса состояний


# -------------------------------------------ХЭНДЛЕР ОБРАБОТКИ КОМАНДЫ /start-----------------------------------------------
def handler_start(bot: AsyncTeleBot):
    @bot.message_handler(commands=['start'])
    async def hi_message(message: Message):
        await bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id) # удаляем состояния пользователя на всякий случай

        # приветственное сообщение
        hello_message: str = """Добро пожаловать! Надеюсь я тебе понравлюсь.\n\nЧто я умею?\n\nТы можешь узнать погоду ☀️ в своём любомом городе, используя мой фунционал. Для этого тебе нужно нажать на кнопку ниже!\n\nК сожалению мне не хватает материальной поддержки, чтобы отправлять тебе погоду из любого населенного пункта планеты(. Поэтому не обижайся, если я не смогу что-то найти❤️)"""
        await bot.send_message(chat_id=message.chat.id, text=hello_message, reply_markup=keyboard.start_markup()) # отправка приветственного сообщения с приветственной клавиатурой
# ----------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------Хендлер нажатия кнопки "Узнать погоду в городе🌆"--------------------------------------------------------
def handler_check_weather_in_city(bot: AsyncTeleBot):
    @bot.message_handler(func = lambda message: message.text=='Узнать погоду в городе🌆')
    async def check_weather_in_users_city(message: Message):
        await bot.send_message(chat_id=message.json['chat']['id'],
                               text='Старайтесь вводить название вашего города🌆 на английском языке (в противном случае я возможно не смогу найти информацию о погоде 🥺)',
                               reply_markup=keyboard.delete_keyboard())
        # отправляем сообщение с пустой клавиатурой


        await bot.set_state(user_id=message.from_user.id, state=States.wait_city, chat_id=message.chat.id) # устанавливаем состояние того, что бот ожидает от пользователя город для установления погоды
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------Хендлер получения погоды по локации--------------------------------------------------------------------------
def handler_get_weather_by_location(bot: AsyncTeleBot):
    @bot.message_handler(content_types=['location'])
    async def get_weather_location(message: Message):
        longitude: float = message.json['location']['longitude']  # вытаскиваем широту
        latitude: float = message.json['location']['latitude']  # вытаскиваем долготу
        await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAM1aBkqNEts3jWS0Yd5HwABUW5Bxu_dAAIhQgACfycxSKvlnJR7gocvNgQ') # отправляем крутой стикер.
        await bot.send_chat_action(chat_id=message.chat.id, action='typing') # отправляем пользоветелю событие, что бот что-то печатает
        weather: dict = await api_weather.get_weather(coords={'longitude': longitude, 'latitude': latitude}) # переменная где хранится погода
        if weather is not None: # если функция вернула истину, то очищаем состояние.
            message_to_send: str = f'🙄Хм... Вы находитесь в каком-то странном под названием <b>{weather['name of place']}</b>\n\nТемпература: {weather['temp']}\nОщущается как {weather['feels_like']}\nСкорость ветра: {weather['windy_speed']}\nПогода: {weather['weather']}'
            await bot.send_message(chat_id=message.chat.id, text=message_to_send) # отправляем сообщение клиенту
            await bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id) # очищаем состояние клиента
        else: # если функция ничего не вернула
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'⛔️ Произошла ошибка при запросе погоды: <b>{Error.last_error.text}</b>. Попробуйте ещё раз! 🔄',
                                   reply_markup=keyboard.stop_trying())
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------Хендлер для получения погоды по городу с состоянием ожидания города------------------------------------
def handler_get_weather_by_city(bot: AsyncTeleBot):
    @bot.message_handler(state=States.wait_city)
    async def get_weather_in_city(city: Message):
        await bot.send_sticker(chat_id=city.chat.id, sticker='CAACAgIAAxkBAAM1aBkqNEts3jWS0Yd5HwABUW5Bxu_dAAIhQgACfycxSKvlnJR7gocvNgQ')
        await bot.send_chat_action(chat_id=city.chat.id, action='typing') # отправляем пользоветелю событие, что бот что-то печатает
        weather_result = await api_weather.get_weather_in_city_api(city) # получаем словарь с результатами погоды
        if weather_result is not None: # если функция вернула истину, то очищаем состояние.
            message_to_send: str = f"""🌆Погода в городе <strong>{city.text}</strong>:\n\nТемпература: {weather_result['temp']}\nОщущается как {weather_result['feels_like']}\nСкорость ветра: {weather_result['windy_speed']}\nПогода: {weather_result['weather']}""" # переменная, которая будет отправлена клиенту
            await bot.send_message(chat_id=city.chat.id, text=message_to_send, reply_markup=keyboard.start_markup()) # отправляем сообщение клиенту
            await bot.delete_state(user_id=city.from_user.id, chat_id=city.chat.id) # очищаем состояние клиента
        else:
            await bot.send_message(chat_id=city.chat.id,
                                   text=f'⛔️ Произошла ошибка при запросе погоды: <b>{Error.last_error.text}</b>. Попробуйте ещё раз! 🔄',
                                   reply_markup=keyboard.stop_trying()) # сообщение об ошибке (вероятно из-за некорректного города)

# -------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------Хендлер обработки при нажатии на кнопку 🔴Прекратить попытки----------------------------------------
def handler_stop_trying_inline_button(bot: AsyncTeleBot):
    @bot.callback_query_handler(func=lambda callback: callback.data == 'stop_trying', state=States.wait_city)
    async def stop_trying_inline_button(callback: CallbackQuery):
        await bot.answer_callback_query(callback_query_id=callback.id) # отвечаем inline кнопке
        user_id: int = callback.from_user.id # id пользователя, который отправил сообщение
        chat_id: int = callback.message.chat.id # id чата
        await bot.delete_state(user_id, chat_id) # удялаем у пользователя состояние
        hello_message: str = """Привет👋.\n\nЧто я умею?\n\nТы можешь узнать погоду ☀️ в своём любомом городе, используя мой фунционал. Для этого тебе нужно нажать на кнопку ниже!\n\nК сожалению мне не хватает материальной поддержки, чтобы отправлять тебе погоду из любого населенного пункта планеты(. Поэтому не обижайся, если я не смогу что-то найти❤️)"""
        await bot.send_message(chat_id=callback.message.chat.id, text=hello_message,
                               reply_markup=keyboard.start_markup())  # отправка приветственного сообщения с приветственной клавиатурой
# ----------------------------------------------------------------------------------------------------------------------------------------------