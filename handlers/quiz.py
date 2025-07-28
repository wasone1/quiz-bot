# handlers/quiz.py

import json
import random
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
import os
from redis.asyncio import Redis


router = Router()

# Завантажуємо питання з файлу
with open("questions.json", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

# Підключення до Redis
REDIS_URL = os.getenv("REDIS_URL")
redis = Redis.from_url(REDIS_URL, decode_responses=True)
print("Підключення до Redis створено")

# Ключі для Redis


def user_score_key(user_id):
    return f"score:{user_id}"


def user_question_key(user_id):
    return f"question:{user_id}"

# Функція для створення inline-клавіатури після відповіді


def get_after_answer_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Наступне питання", callback_data="next_quiz"),
                InlineKeyboardButton(text="Мій рахунок",
                                     callback_data="my_score")
            ]
        ]
    )


def get_score_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Обнулити", callback_data="reset_score")]
        ]
    )

# /start


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Вітаю у вікторині! 🎉\n"
        "Натисни /quiz, щоб отримати питання.\n"
        "Команди:\n"
        "/quiz — нове питання\n"
        "/score — мій рахунок\n"
        "/top — лідерборд\n"
        "/me — моє місце у топі",
    )

# /quiz


@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    question = random.choice(QUESTIONS)
    await redis.set(user_question_key(message.from_user.id), json.dumps(question))
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in question["options"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(question["question"], reply_markup=keyboard)

# Обробка відповіді (НЕ для команд)


@router.message(F.text & ~F.text.startswith("/"))
async def handle_answer(message: types.Message):
    print("Перший запит до Redis")
    q_json = await redis.get(user_question_key(message.from_user.id))
    if not q_json:
        return
    question = json.loads(q_json)
    answer = message.text.strip().lower()
    correct = question["answer"].strip().lower()
    user_id = message.from_user.id
    user_name = message.from_user.full_name or f"User {user_id}"
    await redis.set(f"user_name:{user_id}", user_name)
    if answer == correct:
        await redis.incr(user_score_key(user_id))
        text = "✅ Вірно! +1 бал 🎉"
    else:
        text = f"❌ Невірно! Правильна відповідь: {question['answer']}"
    await message.answer(text, reply_markup=get_after_answer_keyboard())
    await redis.delete(user_question_key(user_id))

# Callback: Наступне питання


@router.callback_query(lambda c: c.data == "next_quiz")
async def callback_next_quiz(callback: CallbackQuery):
    question = random.choice(QUESTIONS)
    await redis.set(user_question_key(callback.from_user.id), json.dumps(question))
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in question["options"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await callback.message.answer(question["question"], reply_markup=keyboard)
    await callback.answer()

# Callback: Мій рахунок


@router.callback_query(lambda c: c.data == "my_score")
async def callback_my_score(callback: CallbackQuery):
    score = await redis.get(user_score_key(callback.from_user.id))
    score = int(score) if score else 0
    await callback.message.answer(
        f"Твій рахунок: {score} балів",
        reply_markup=get_score_keyboard()
    )
    await callback.answer()

# /score


@router.message(Command("score"))
async def cmd_score(message: types.Message):
    score = await redis.get(user_score_key(message.from_user.id))
    score = int(score) if score else 0
    await message.answer(
        f"Твій рахунок: {score} балів",
        reply_markup=get_score_keyboard()
    )


@router.callback_query(lambda c: c.data == "reset_score")
async def callback_reset_score(callback: CallbackQuery):
    await redis.delete(user_score_key(callback.from_user.id))
    await callback.message.answer("Твій рахунок обнулено! Починай спочатку 🎲")
    await callback.answer()
    
# /top


@router.message(Command("top"))
async def cmd_top(message: types.Message):
    keys = await redis.keys("score:*")
    scores = []
    for key in keys:
        user_id = key.split(":")[1]
        score = int(await redis.get(key) or 0)
        # Отримуємо ім'я користувача
        user_name = await redis.get(f"user_name:{user_id}") or f"User {user_id}"
        scores.append((user_name, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    text = "🏆 Лідерборд:\n"
    for i, (user_name, score) in enumerate(scores[:10], 1):
        text += f"{i}. {user_name}: {score} балів\n"
    if not scores:
        text += "Поки що немає гравців."
    await message.answer(text)


@router.message(Command("me"))
async def cmd_me(message: types.Message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.full_name or f"User {user_id}"
    keys = await redis.keys("score:*")
    scores = []
    for key in keys:
        uid = key.split(":")[1]
        score = int(await redis.get(key) or 0)
        scores.append((uid, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    place = next((i+1 for i, (uid, _) in enumerate(scores)
                 if uid == user_id), None)
    my_score = await redis.get(user_score_key(user_id)) or 0
    if place:
        await message.answer(f"{user_name}, твоє місце у топі: {place}\nТвій рахунок: {my_score} балів")
    else:
        await message.answer("Ти ще не у топі. Відповідай на питання, щоб потрапити у лідерборд!")
