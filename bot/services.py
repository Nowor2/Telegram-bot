import aiohttp

class HTTPClient:
    def __init__(self):
        self.session = None

    async def start(self):
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()


class DictionaryService:
    def __init__(self, config, http):
        self.config = config
        self.http = http

    async def get(self, word):
        async with self.http.session.get(
            self.config.DICTIONARY_API + word
        ) as r:
            if r.status != 200:
                return None
            return await r.json()


class TranslationService:
    def __init__(self, config, http):
        self.config = config
        self.http = http

    async def translate(self, word):
        async with self.http.session.get(
            self.config.TRANSLATION_API,
            params={"q": word, "langpair": "en|uk"}
        ) as r:
            if r.status != 200:
                return "error"
            data = await r.json()
            return data["responseData"]["translatedText"]