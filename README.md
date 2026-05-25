English Learning Telegram Bot

Сучасний асинхронний Telegram-бот для вивчення англійських слів з використанням:

перекладу EN → UA

визначення слова

транскрипції

прикладів використання

Redis кешу

SQLite бази даних

SHA-256 хешування

Fernet шифрування

аналітики та графіків



---

🚀 Основні можливості

📘 Інформація про слово

Бот показує:

переклад

транскрипцію

частину мови

визначення слова

приклад використання


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


---

🛠 Використані технології

Технологія	Призначення

Aiogram	Telegram framework
Redis	Кешування
SQLite	База даних
aiohttp	Async HTTP запити
cryptography	Шифрування
pandas	Аналітика
matplotlib	Графіки
dotenv	Змінні середовища



---

🧠 Архітектура проєкту

Telegram User
       ↓
Aiogram Bot
       ↓
Redis Cache (hashed keys)
       ↓
Dictionary API
       ↓
SQLite Database (encrypted)
       ↓
Analytics


---

🔐 Безпека

SHA-256 Hashing

Слова хешуються перед записом у Redis.

Приклад:

word:cbd31fe312a05a4718b4d67151a8c4052c9aa091f4012fbf5a77ba5da8df41ef


---

Fernet Encryption

У SQLite шифруються:

user_id

слово

переклад


Приклад encrypted даних:

gAAAAABq...


---

📦 Встановлення

1. Клонування проєкту

git clone <repository_url>
cd project


---

2. Створення virtual environment

Windows

python -m venv .venv
.venv\Scripts\activate

Linux/macOS

python3 -m venv .venv
source .venv/bin/activate


---

3. Встановлення залежностей

pip install -r requirements.txt


---

⚡ Встановлення Redis

Через Docker

docker run -p 6379:6379 redis


---

Перевірка Redis

redis-cli ping

Очікуваний результат:

PONG


---

⚙️ Налаштування .env

Створи файл .env

BOT_TOKEN=your_bot_token

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

DICTIONARY_API=https://api.dictionaryapi.dev/api/v2/entries/en/
TRANSLATION_API=https://api.mymemory.translated.net/get

SECRET_KEY=your_fernet_key


---

🔑 Генерація SECRET_KEY

Запусти один раз:

from cryptography.fernet import Fernet

print(Fernet.generate_key().decode())

Встав отриманий ключ у .env


---

▶️ Запуск бота

python main.py


---

📌 Команди бота

Команда	Опис

/start	Запуск бота
/help	Допомога
/stats	Статистика
/chart	Графік популярних слів



---

⚡ Система кешування

Перший запит слова

❌ CACHE MISS
💾 CACHE SAVED

Бот звертається до API та зберігає результат у Redis.


---

Повторний запит

✅ CACHE HIT

Дані беруться прямо з Redis без API.


---

🗄 База даних

SQLite база:

bot.db

Містить encrypted історію пошуку слів.


---

📊 Аналітика

Бот вміє показувати:

кількість слів

кількість користувачів

топ популярних слів

графіки


Приклад:

📊 Stats

Words: 54
Users: 8

apple: 12
hello: 9
world: 6


---

📁 Структура проєкту

project/
│
├── main.py
├── config.py
├── handlers.py
├── cache.py
├── db.py
├── services.py
├── security.py
├── analytics.py
├── requirements.txt
├── .env
└── bot.db


---

🔮 Можливі покращення

У майбутньому можна додати:

PostgreSQL

Docker Compose

Admin panel

Web dashboard

Авторизацію

Rate limiting

CI/CD

Unit tests

VPS deployment
