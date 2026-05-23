import json
import redis.asyncio as redis


class RedisCache:
    def __init__(self, config):

        self.client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=True
        )

    # ================= GET =================
    async def get(self, key):

        try:
            data = await self.client.get(key)

            if data is None:
                print(f"❌ CACHE MISS: {key}")
                return None

            print(f"✅ CACHE HIT: {key}")

            return json.loads(data)

        except Exception as e:

            print("❌ CACHE GET ERROR:", e)

            return None

    # ================= SET =================
    async def set(self, key, value, ttl):

        try:
            serialized = json.dumps(
                value,
                ensure_ascii=False,
                default=str
            )

            await self.client.set(
                key,
                serialized,
                ex=ttl
            )

            print(f"💾 CACHE SAVED: {key}")

        except Exception as e:

            print("❌ CACHE SET ERROR:", e)

    # ================= DELETE =================
    async def delete(self, key):

        try:
            await self.client.delete(key)
            print(f"🗑 CACHE DELETED: {key}")
        except Exception as e:
            print("❌ CACHE DELETE ERROR:", e)

    # ================= PING =================
    async def ping(self):

        try:
            await self.client.ping()
            print("✅ Redis connected")
        except Exception as e:
            print("❌ Redis connection error:", e)

    # ================= CLOSE =================
    async def close(self):

        try:
            await self.client.close()
        except Exception as e:
            print("❌ CACHE CLOSE ERROR:", e)