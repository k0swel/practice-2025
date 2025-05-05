from dotenv import find_dotenv, load_dotenv
import os
import requests
from error import Error # импортирую собственный класс для ошибок

load_dotenv(find_dotenv()) # загружаем переменные из .env
API: str = os.getenv(key='weather_api') # сохраняем api_ключ сервиса получения погоды в переменной

def get_coords(city: str) -> dict:
    load_dotenv(dotenv_path=find_dotenv())  # загружаем переменные из виртуального окружения
    URL: str = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API}' #ссылка для запроса
    request_to_get_coords: list = requests.get(url=URL).json()  # ответ на запрос координат по городу
    if len(request_to_get_coords) == 0: ## если список ответа ничем не заполнен - значит мы ввели неверный город
        raise Error(text='Город введён некорректно!')
    else:
        lat: int = request_to_get_coords[0]['lat']  # широта
        lon: int = request_to_get_coords[0]['lon']  # долгота

        return_variable: dict = {'lat': lat, 'lon': lon, 'city': city}
        return return_variable


def get_weather(coords: dict, time: str, units: str) -> dict: # units = единица измерения температуры. metric = цельсии, imperial = фаренгеит, standard = калвины
    return_variable: dict # значение, которое будет возвращать функция

    if time == 'now': #если нужно получить погоду в данный момент времени
        URL: str = f'https://api.openweathermap.org/data/2.5/weather?lat={coords.get('lat')}&lon={coords.get('lon')}&appid={API}&units={units}'
        request_to_get_weather: dict = requests.get(url=URL).json() # ответ на запрос
        return_variable = {'temp': round(request_to_get_weather['main']['temp'], 0), # температура в цельсиях
                           'feels_like': round(request_to_get_weather['main']['feels_like'], 0), # насколько ощущается погода
                           'windy_speed': request_to_get_weather['wind']['speed'], # скорость ветра км/ч
                           'weather': request_to_get_weather['weather'][0]['main'] # описание погоды
                           }
        return return_variable
    else:
        URL: str = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={coords.get('lat')}&lon={coords.get('lon')}&appid={API}'
        request_to_get_weather: dict = requests.get(url=URL).json()  # ответ на запрос
        print(request_to_get_weather)




