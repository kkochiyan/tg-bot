import requests
import app.keyboards as kb

import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={os.getenv('API_ID')}'
        res = requests.get(url)
        if res.status_code == 200:
            weather_data = requests.get(url).json()
            temperature = round(weather_data['main']['temp'])
            return f'Температура в городе {city} : {str(temperature)} °C', 'Сохранить город?', kb.save_or_no
        else:
            return f'Произошла ошибка\nСтатус код ошибки: {res.status_code}', 'Выберите действие', kb.submenu
    except Exception as e:
        return f'Произошла ошибка {type(e)} при подключении к серверу', 'Выберите действие', kb.submenu


def get_saves_weathers(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={os.getenv('API_ID')}'
        res = requests.get(url)
        if res.status_code == 200:
            weather_data = requests.get(url).json()
            temperature = round(weather_data['main']['temp'])
            return f'Температура в городе {city} : {str(temperature)} °C'
        else:
            return f'Произошла ошибка\nСтатус код ошибки: {res.status_code}'
    except Exception as e:
        return f'Произошла ошибка {type(e)} при подключении к серверу'
