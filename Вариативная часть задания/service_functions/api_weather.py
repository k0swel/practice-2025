from dotenv import find_dotenv, load_dotenv # библиотеки для переменных виртуального окружения
import os # библиоетка для переменных виртуального окружения
from aiohttp import ClientSession # для get-запросов к ресурсу с погодой
from service_functions.custom_error import Error # кастомый класс ошибки
from telebot.types import Message # импорт класса сообщений телеграм

# -------------------------------------------СЛУЖЕБНЫЕ ПЕРЕМЕННЫЕ------------------------------------------
load_dotenv(find_dotenv()) # обновляем виртуальные переменные процесса
API: str = os.getenv(key='weather_api') # сохраняем api_ключ сервиса получения погоды в переменной
# ---------------------------------------------------------------------------------------------------------



# ---------------------------------------API получения координат по введенному городу--------------------------
async def get_coords(city: str) -> dict:
    load_dotenv(dotenv_path=find_dotenv())  # загружаем переменные из виртуального окружения
    URL: str = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API}' #ссылка для запроса
    async with ClientSession() as Session:
        async with Session.get(url=URL) as responce:
            request_to_get_coords = await responce.json()
    if len(request_to_get_coords) == 0: ## если список ответа ничем не заполнен - значит мы ввели неверный город
        raise Error(error_text='Город введен некорректно')
    else:
        lat: int = request_to_get_coords[0]['lat']  # широта
        lon: int = request_to_get_coords[0]['lon']  # долгота

        return_variable: dict = {'latitude': lat, 'longitude': lon, 'city': city}
        return return_variable
# -------------------------------------------------------------------------------------------------------------


# -------------------------------------------------API для получения погоды------------------------------------
async def get_weather(coords: dict[str, int], units: str = 'metric', time: str = 'now') -> dict | None: # units = единица измерения температуры. metric = цельсии, imperial = фаренгеит, standard = калвины
    return_variable: dict # значение, которое будет возвращать функция

    if time == 'now': #если нужно получить погоду в данный момент времени
        URL: str = f'https://api.openweathermap.org/data/2.5/weather?lat={coords.get('latitude')}&lon={coords.get('longitude')}&appid={API}&units={units}'
        async with ClientSession() as Session:
            async with Session.get(url=URL) as responce:
                request_to_get_weather = await responce.json()
        responce_from_request = {'temp': int(request_to_get_weather['main']['temp']), # температура в цельсиях
                           'feels_like': int(request_to_get_weather['main']['feels_like']), # насколько ощущается погода
                           'windy_speed': int(request_to_get_weather['wind']['speed']), # скорость ветра км/ч
                           'weather': request_to_get_weather['weather'][0]['main'], # описание погоды
                           "name of place": request_to_get_weather['name'] # город
                           }
        return fill_weather_dict(responce_from_request)
    else:
        return None
# ------------------------------------------------------------------------------------------------------------


# -----------------------------------------------Получение погоды по городу----------------------------
async def get_weather_in_city_api(message: Message) -> dict:
    city: str = message.text # устанавливаем значение города
    weather_dict = dict() # возвращаемая хеш таблица
    try:
        weather: dict = await get_weather(await get_coords(city), time='now', units='metric') # обрабатываем событие если мы ввели город неверно.
    except Error as er:
        return None # если произошла ошибка при получении погоды
    return weather
# ------------------------------------------------------------------------------------------------------------------------------


def fill_weather_dict(weather_responce_from_http: dict) -> dict:
    weather: dict = dict() # возвращаемое значени
    # -------------Фактическая температура и как ощущается---------
    if weather_responce_from_http['feels_like'] < 13:  # если температура меньше 13 по цельсию
        weather['temp'] = str(weather_responce_from_http['feels_like']) + '°C 🥶'
        weather['feels_like'] = str(weather_responce_from_http['feels_like']) + ' °C 🥶'
    elif 13 <= weather_responce_from_http['feels_like'] <= 22:  # если температура между 13 и 22 по цельсию
        weather['temp'] = str(weather_responce_from_http['feels_like']) + '°C 🤗'
        weather['feels_like'] = str(weather_responce_from_http['feels_like']) + ' °C 🤗'
    else:  # если жарко
        weather['temp'] = str(weather_responce_from_http['feels_like']) + '🔥'
        weather['feels_like'] = str(weather_responce_from_http['feels_like']) + ' °C 🔥'
    # ------------------------------------------------------------

    # ------------------------Скорость ветра----------------------
    if weather_responce_from_http['windy_speed'] < 10:
        weather['windy_speed'] = str(weather_responce_from_http['feels_like']) + ' км/ч 🐢'
    else:
        weather['windy_speed'] = str(weather_responce_from_http['feels_like']) + ' км/ч 💨'
    # -----------------------------------------------------------

    # --------------Погода (солнечно, ветренно и.т.п)-------------
    if weather_responce_from_http['weather'] == 'Rain':
        weather['weather'] = 'Дождь 🌧'
    elif weather_responce_from_http['weather'] == 'Snow':
        weather['weather'] = 'Идёт снег ❄️'
    elif weather_responce_from_http['weather'] == 'Clouds':
        weather['weather'] = 'Облачно ☁️'
    elif weather_responce_from_http['weather'] == 'Clear':
        weather['weather'] = 'Ясно ☁️❌'
    else:
        weather['weather_str'] = weather['weather']
    # --------------------------------------------------------

    if weather_responce_from_http.get("name of place") is not None: # если в http-ответе присутствует информация о месте погоды
        weather['name of place'] = weather_responce_from_http['name of place']
    return weather




