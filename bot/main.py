import asyncio
from aiogram import Bot, Dispatcher

from config import Config
from security import SecurityService
from cache import RedisCache
from db import Database
from services import HTTPClient, DictionaryService, TranslationService
from analytics import Analytics
from handlers import Handlers


class BotApp:
    def __init__(self):
        self.config = Config()

        self.bot = Bot(self.config.BOT_TOKEN)
        self.dp = Dispatcher()

        self.security = SecurityService(self.config.SECRET_KEY)

        self.cache = RedisCache(self.config)
        self.db = Database(self.security)

        self.http = HTTPClient()

        self.dict = DictionaryService(self.config, self.http)
        self.trans = TranslationService(self.config, self.http)

        self.analytics = Analytics(self.db)

        Handlers(
            self.dp,
            self.cache,
            self.db,
            self.dict,
            self.trans,
            self.analytics,
            self.security,
            self.config
        )

    async def run(self):
        await self.http.start()
        await self.db.init()
        await self.cache.ping()

        try:
            await self.dp.start_polling(self.bot)
        finally:
            await self.http.close()
            await self.cache.close()


async def main():
    app = BotApp()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())