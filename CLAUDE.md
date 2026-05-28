# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All commands run from the `bot/` directory with the virtual environment activated.

**Setup:**
```bash
# Windows
.venv\Scripts\activate
pip install -r bot/requirements.txt

# Generate a Fernet SECRET_KEY (one-time)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Run the bot:**
```bash
cd bot && python main.py
```

**Redis (required before starting):**
```bash
docker run -p 6379:6379 redis
```

## Environment Variables

Create `bot/.env` (or project root `.env`):
```env
BOT_TOKEN=
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
DICTIONARY_API=https://api.dictionaryapi.dev/api/v2/entries/en/
TRANSLATION_API=https://api.mymemory.translated.net/get
SECRET_KEY=   # Fernet key, base64-encoded 32-byte key
CACHE_TTL=86400
```

## Architecture

`BotApp` in `main.py` wires all services together and passes them into `Handlers`. There is no DI framework — dependencies flow explicitly through constructors.

**Request flow for a word lookup:**
1. `Handlers.word()` receives the message
2. The word is SHA-256 hashed (`SecurityService.hash_text`) to form the Redis key `word:<hash>`
3. Cache hit → return cached JSON; cache miss → call `DictionaryService` + `TranslationService`
4. Result is stored in Redis with TTL from config
5. `Database.log_word()` stores an **encrypted** copy (Fernet) of user_id, word, and translation in SQLite

**Security model:** All data at rest in SQLite is Fernet-encrypted. Redis keys use SHA-256 hashes of words (not the plaintext). The same `SecurityService` handles both; it requires a valid base64 Fernet key in `SECRET_KEY` — a wrong or missing key will cause decrypt errors at runtime.

**Analytics:** `Analytics` class reads from `Database` and either returns a formatted text string (`/stats`) or generates a `chart.png` bar chart via matplotlib (`/chart`). The chart file is written to the working directory and sent as a photo.

**Callback data format:** Inline keyboard buttons encode the plaintext word: `refresh:<word>` and `clear:<word>`. The word is re-hashed on each callback to look up the Redis key.

**`db_path` default is `"bot.db"`** — a relative path, so the database is created in whatever directory `main.py` is run from (project root when run as `cd bot && python main.py` places it inside `bot/`, but the existing `bot.db` is at the project root).
