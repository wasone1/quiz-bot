# Telegram Quiz Bot

> Сучасний Telegram-бот-вікторина з веб-лідербордом, історією балів та деплоєм на Railway.

Бот-вікторина на Python (aiogram 3.x + Redis + Flask) з підрахунком балів, лідербордом та веб-інтерфейсом.

## Функціонал

- Вікторина з питаннями (з варіантами або відкритими)
- Підрахунок балів для кожного користувача
- Лідерборд у Telegram (/top) та на веб-сайті
- Перегляд свого рахунку (/score)
- FSM (Finite State Machine) для сценаріїв
- Redis для зберігання стану та балів
- Веб-сайт лідерборду: [Відкрити у браузері](https://practical-success-production.up.railway.app)

## Технології

- Python 3.10+
- aiogram
- redis
- flask
- gunicorn
- python-dotenv

## Запуск локально

1. Клонувати репозиторій:
    ```
    git clone https://github.com/yourusername/quiz-bot.git
    cd quiz-bot
    ```
2. Встановити залежності:
    ```
    pip install -r requirements.txt
    ```
3. Запустити Redis (локально або через Docker):
    ```
    docker run -p 6379:6379 redis
    ```
4. Створити файл `.env` на основі `.env.example` і додати токен бота та налаштування Redis:
    ```
    BOT_TOKEN=тут_твій_токен
    REDIS_URL=redis://localhost:6379/0
    ```
5. Запустити бота:
    ```
    python main.py
    ```
6. Запустити веб-лідерборд:
    ```
    python web_stats.py
    ```
    або для продакшну:
    ```
    gunicorn web_stats:app --bind 0.0.0.0:5000
    ```

## Деплой на Railway

1. Форкни або клонуй цей репозиторій.
2. Задеплой проект на [Railway](https://railway.app/) через "Deploy from GitHub repo".
3. Додай змінні середовища (Variables) для кожного сервісу:
    - `BOT_TOKEN` — токен твого Telegram-бота (для бота)
    - `REDIS_URL` — URL твого Redis (Railway додасть автоматично)
4. Для веб-інтерфейсу вкажи Start Command:
    ```
    gunicorn web_stats:app --bind 0.0.0.0:5000
    ```
5. Для бота вкажи Start Command:
    ```
    python main.py
    ```
6. Після деплою веб-лідерборд буде доступний за посиланням:
    ```
    https://practical-success-production.up.railway.app
    ```

## Приклад команд

- `/start` — почати вікторину
- `/quiz` — нове питання
- `/score` — мій рахунок
- `/top` — лідерборд
- `/me` — моє місце у топі

## Як додати питання

Питання зберігаються у файлі `questions.json` у форматі:
```json
[
  {
    "question": "Яка столиця Франції?",
    "options": ["Париж", "Берлін", "Мадрид", "Рим"],
    "answer": "Париж"
  }
]

## Посилання

- [Веб-лідерборд](https://practical-success-production.up.railway.app)
<!-- - [Бот у Telegram](https://t.me/MyTestTelegramQuizbot) -->

## Ліцензія

MIT License