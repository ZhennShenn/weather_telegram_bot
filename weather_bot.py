import requests
import datetime as dt
from pprint import pprint
from config import open_weather_token


def get_weather(city, token):

    emoji = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
           f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric&lang=ru"
        )
        data = r.json()
        # pprint(data)
        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data["weather"][0]["main"]
        if weather_description in emoji:
            wd = emoji[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = dt.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = dt.datetime.fromtimestamp(data['sys']['sunset'])

        print(f"***{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}***"
              f"Погода в городе: {city}\nТемпература: {cur_weather} C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
              f"Ветер: {wind} м.с\nВосход солнца: {sunrise_timestamp}\nЗаход солнца: {sunset_timestamp}\n"
              f"Хорошего дня!")

    except Exception as ex:
        print(ex)
        print('Проверьте название города')


def main():
    city = input('Введите ваш город: ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
