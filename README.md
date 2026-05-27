English Learning Telegram Bot

Сучасний асинхронний Telegram-бот для вивчення англійської мови з використанням:

Redis Cache
SQLite Database
SQL Queries
Encryption & Hashing
Analytics System
Async Architecture
🚀 Основні можливості
📘 Інформація про слово

Бот показує:

🇺🇦 переклад
🔊 транскрипцію
📚 частину мови
📖 визначення
✏️ приклад використання
Приклад:
📘 Word:
Apple

🇺🇦 Translation:
Яблуко

🔊 Phonetic:
/ˈæp.əl/

📚 Part of Speech:
noun

📖 Definition:
A round fruit with red or green skin.

✏️ Example:
I eat an apple every morning.
⚡ Кешування через Redis

Бот використовує Redis для швидкого кешування слів.

Перший запит:
❌ CACHE MISS
💾 CACHE SAVED

Бот звертається до API та зберігає результат.

Повторний запит:
✅ CACHE HIT

Дані беруться з Redis без повторного API-запиту.

🗄 База даних SQLite

Проєкт використовує SQLite (bot.db).

📋 Таблиці
users
Поле	Тип
id	INTEGER
telegram_id	TEXT
created_at	TEXT
history
Поле	Тип
id	INTEGER
user_id	TEXT
word	TEXT
translation	TEXT
created_at	TEXT
🔥 SQL Queries

У проєкті використовуються:

CREATE TABLE
CREATE TABLE IF NOT EXISTS users (...)
INSERT
INSERT INTO history (...)
VALUES (?, ?, ?, ?)
SELECT
SELECT word FROM history
COUNT
SELECT COUNT(*) FROM history
ORDER BY
ORDER BY id DESC
LIMIT
LIMIT 5
🔐 Безпека
SHA-256 Hashing

Redis keys хешуються через SHA-256.

Приклад:
word:cbd31fe312a05a4718b4d67151a8c4052c9aa091f4012fbf5a77ba5da8df41ef
Fernet Encryption

У SQLite шифруються:

user_id
слово
переклад
Приклад encrypted значення:
gAAAAABq...
📊 Аналітика

Бот підтримує:

статистику
топ слів
кількість користувачів
останні пошуки
графіки
Команда /stats

Показує:

загальну кількість слів
кількість користувачів
топ слів
останні пошуки
Команда /chart

Генерує графік популярних слів.

🛠 Використані технології
Технологія	Призначення
Python	Backend
Aiogram	Telegram Bot Framework
Redis	Cache
SQLite	Database
aiosqlite	Async SQL
aiohttp	HTTP requests
cryptography	Encryption
pandas	Analytics
matplotlib	Charts
🧠 Архітектура проєкту
Telegram User
       ↓
Aiogram Bot
       ↓
Redis Cache
       ↓
Dictionary API
       ↓
SQLite Database
       ↓
Analytics System
📦 Встановлення
1. Клонування проєкту
git clone <repository_url>
cd project
2. Створення virtual environment
Windows
python -m venv .venv
.venv\Scripts\activate
Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
3. Встановлення залежностей
pip install -r requirements.txt
⚡ Встановлення Redis
Docker
docker run -p 6379:6379 redis
Перевірка Redis
redis-cli ping

Результат:

PONG
⚙️ Налаштування .env

Створи .env

BOT_TOKEN=your_bot_token

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

DICTIONARY_API=https://api.dictionaryapi.dev/api/v2/entries/en/
TRANSLATION_API=https://api.mymemory.translated.net/get

SECRET_KEY=your_fernet_key
🔑 Генерація SECRET_KEY
from cryptography.fernet import Fernet

print(Fernet.generate_key().decode())
▶️ Запуск бота
python main.py
📌 Команди
Команда	Опис
/start	Запуск бота
/help	Допомога
/stats	Статистика
/chart	Графік
📁 Структура проєкту
project/
│
├── main.py
├── config.py
├── handlers.py
├── cache.py
├── db.py
├── analytics.py
├── security.py
├── services.py
├── requirements.txt
├── .env
└── bot.db
