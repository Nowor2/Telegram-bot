import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 6379))

    DICTIONARY_API = os.getenv("DICTIONARY_API")
    TRANSLATION_API = os.getenv("TRANSLATION_API")

    SECRET_KEY = os.getenv("SECRET_KEY")

    CACHE_TTL = int(os.getenv("CACHE_TTL", 86400))