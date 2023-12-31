import requests
import datetime as dt
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши название города и я пришлю сводку погоды!")


@dp.message_handler()
async def det_weather(message: types.Message):
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
           f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru"
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

        await message.reply(f"***{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}***"
              f"Погода в городе: {city}\nТемпература: {cur_weather} C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
              f"Ветер: {wind} м.с\nВосход солнца: {sunrise_timestamp}\nЗаход солнца: {sunset_timestamp}\n"
              f"Хорошего дня!")

    except:
        await message.reply('\U00002620 Проверьте название города \U00002620')

if __name__ == '__main__':
    executor.start_polling(dp)