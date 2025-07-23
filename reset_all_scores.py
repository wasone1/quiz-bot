import asyncio
from redis.asyncio import Redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


async def reset_all_scores():
    redis = Redis(host=REDIS_HOST, port=REDIS_PORT,
                  db=REDIS_DB, decode_responses=True)
    keys = await redis.keys("score:*")
    if keys:
        await redis.delete(*keys)
        print(f"Всі рахунки ({len(keys)}) обнулено!")
    else:
        print("Немає рахунків для обнулення.")

if __name__ == "__main__":
    asyncio.run(reset_all_scores())
