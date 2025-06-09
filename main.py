
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import requests
from settings import BOT_TOKEN, OPENWEATHER_API_KEY


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! 👋 Я бот, который показывает погоду.\n"
        "Просто напиши название города, и я пришлю текущую температуру и погоду."
    )

# Обработчик текстовых сообщений (название города)
@dp.message(F.text)
async def get_weather(message: types.Message):
    city = message.text.strip()
    try:
        # Запрос к OpenWeather API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
        response = requests.get(url).json()

        # Проверка на ошибки
        if response.get("cod") != 200:
            error_msg = response.get("message", "Неизвестная ошибка")
            await message.answer(f"❌ Ошибка: {error_msg.capitalize()}")
            return

        # Парсим данные
        weather_desc = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        feels_like = response["main"]["feels_like"]
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]

        # Формируем ответ
        weather_info = (
            f"🌆 Город: {city}\n"
            f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"☁ Погода: {weather_desc.capitalize()}\n"
            f"💧 Влажность: {humidity}%\n"
            f"🌬 Ветер: {wind_speed} м/с"
        )

        await message.answer(weather_info)

    except Exception as e:
        await message.answer("❌ Произошла ошибка. Попробуйте позже или проверьте название города.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())