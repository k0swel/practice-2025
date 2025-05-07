from telebot.types import Message
from error import Error
from api_weather import get_coords
from main import Bot
import keyboard
import api_weather

async def send_weather_by_city(message: Message) -> bool:
    city: str = message.text # устанавливаем значение города
    try:
        weather: dict = await api_weather.get_weather(await get_coords(city), time='now', units='metric') # обрабатываем событие если мы ввели город неверно.
    except Error as er:
        await Bot.send_message(chat_id = message.chat.id, text=f'⛔️ Произошла ошибка при запросе погоды: <b>{er.text_error()}</b>. Попробуйте ещё раз! 🔄', reply_markup=keyboard.stop_trying())
        return False
    if weather['feels_like'] < 13:  # если температура меньше 13 по цельсию
        temp: str = str(weather['temp']) + '°C 🥶'
        feels_like: str = str(weather['feels_like']) + ' °C 🥶'
    elif 13 <= weather['feels_like'] <= 22:  # если температура между 13 и 22 по цельсию
        temp: str = str(weather['temp']) + '🤗'
        feels_like: str = str(weather['feels_like']) + ' °C 🤗'
    else:  # если жарко
        temp: str = str(weather['temp']) + '🔥'
        feels_like: str = str(weather['feels_like']) + ' °C 🔥'
    ## Скорость ветра
    if weather['windy_speed'] < 10:
        windy_speed: str = str(weather['windy_speed']) + ' км/ч 🐢'
    else:
        windy_speed: str = str(weather['windy_speed']) + ' км/ч 💨'

    if weather['weather'] == 'Rain':
        weather_str: str = 'Дождь 🌧'
    elif weather['weather'] == 'Snow':
        weather_str: str = 'Идёт снег ❄️'
    elif weather['weather'] == 'Clouds':
        weather_str: str = 'Облачно ☁️'
    elif weather['weather'] == 'Clear':
        weather_str: str = 'Ясно ☁️❌'
    else:
        weather_str: str = weather['weather']
    await Bot.send_message(chat_id=message.chat.id, text=f'🌆Погода в городе <b>{message.text}</b>:\n\nТемпература: {temp}\nОщущается как {feels_like}\nСкорость ветра: {windy_speed}\nПогода: {weather_str}', reply_markup=keyboard.start_markup()) # печатаем сообщение пользователю
    return True


async def send_weather_by_location(message: Message) -> None:
    longitude: int = message.json['location']['longitude']  # вытаскиваем широту
    latitude: int = message.json['location']['latitude']  # вытаскиваем долготу
    weather: dict = await api_weather.get_weather(coords={'longitude': longitude, 'latitude': latitude}, time='now',
                                            units='metric')  # узнаём погоду
    ## Температура
    if weather['feels_like'] < 13:  # если температура меньше 13 по цельсию
        temp: str = str(weather['temp']) + '°C 🥶'
        feels_like: str = str(weather['feels_like']) + ' °C 🥶'
    elif 13 <= weather['feels_like'] <= 22:  # если температура между 13 и 22 по цельсию
        temp: str = str(weather['temp']) + '🤗'
        feels_like: str = str(weather['feels_like']) + ' °C 🤗'
    else:  # если жарко
        temp: str = str(weather['temp']) + '🔥'
        feels_like: str = str(weather['feels_like']) + ' °C 🔥'
    ## Скорость ветра
    if weather['windy_speed'] < 10:
        windy_speed: str = str(weather['windy_speed']) + ' км/ч 🐢'
    else:
        windy_speed: str = str(weather['windy_speed']) + ' км/ч 💨'

    if weather['weather'] == 'Rain':
        weather_str: str = 'Дождь 🌧'
    elif weather['weather'] == 'Snow':
        weather_str: str = 'Идёт снег ❄️'
    elif weather['weather'] == 'Clouds':
        weather_str: str = 'Облачно ☁️'
    elif weather['weather'] == 'Clear':
        weather_str: str = 'Ясно ☁️❌'
    else:
        weather_str: str = weather['weather']
    await Bot.send_message(chat_id=message.json['chat']['id'], text=f'🙄Хм... Вы находитесь в каком-то странном под названием <b>{weather['name of place']}</b>\n\nТемпература: {temp}\nОщущается как {feels_like}\nСкорость ветра: {windy_speed}\nПогода: {weather_str}') # печатаем сообщение пользователю
