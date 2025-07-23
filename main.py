# main.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import quiz


async def main():
    if not BOT_TOKEN:
        print("❌ Помилка: BOT_TOKEN не знайдено! Додайте токен у .env файл.")
        return

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Додаємо меню команд
    commands = [
        BotCommand(command="start", description="Почати вікторину"),
        BotCommand(command="quiz", description="Нове питання"),
        BotCommand(command="score", description="Мій рахунок"),
        BotCommand(command="top", description="Лідерборд"),
        BotCommand(command="me", description="Моє місце у топі"),
    ]
    await bot.set_my_commands(commands)
    
	 # Підключаємо роутери
    dp.include_router(quiz.router)

    print("Бот-вікторина запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
