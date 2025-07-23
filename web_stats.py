import asyncio
from flask import Flask, render_template_string
from redis.asyncio import Redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Лідерборд вікторини</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f7f7f7; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 60%; margin: 30px auto; background: #fff; }
        th, td { border: 1px solid #ccc; padding: 10px 20px; text-align: center; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h1 align="center">🏆 Лідерборд вікторини</h1>
    <table>
        <tr>
            <th>Місце</th>
            <th>Ім'я</th>
            <th>Рахунок</th>
        </tr>
        {% for user in users %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ user[0] }}</td>
            <td>{{ user[1] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


async def get_top_users():
    redis = Redis(host=REDIS_HOST, port=REDIS_PORT,
                  db=REDIS_DB, decode_responses=True)
    keys = await redis.keys("score:*")
    scores = []
    for key in keys:
        user_id = key.split(":")[1]
        score = int(await redis.get(key) or 0)
        user_name = await redis.get(f"user_name:{user_id}") or f"User {user_id}"
        scores.append((user_name, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:10]


@app.route("/")
def leaderboard():
    users = asyncio.run(get_top_users())
    return render_template_string(HTML, users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
