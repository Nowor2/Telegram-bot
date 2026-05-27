# 📘 English Learning Telegram Bot

Сучасний асинхронний Telegram-бот для вивчення англійської мови.

Бот використовує:

- Aiogram
- Redis Cache
- SQLite Database
- Encryption & Hashing
- Analytics System
- Async Architecture

---

# 🚀 Основні можливості

## 📚 Інформація про слово

Бот показує:

- 🇺🇦 переклад
- 🔊 транскрипцію
- 📖 значення слова
- 📚 частину мови
- ✏️ приклад використання

---

## ⚡ Redis Cache

Бот кешує слова через Redis.

### Приклад:

```text
❌ CACHE MISS
💾 CACHE SAVED
```

Повторний запит:

```text
✅ CACHE HIT
```

---

## 🗄 SQLite Database

Бот зберігає:

- користувачів
- історію пошуків
- дату запиту

---

## 🔐 Encryption + Hashing

### Hashing

Redis keys хешуються через SHA-256.

### Encryption

SQLite дані шифруються через Fernet:

- user_id
- word
- translation

---

## 📊 Аналітика

Бот підтримує:

- статистику
- топ слів
- графіки
- кількість користувачів

---

# 🛠 Використані технології

| Технологія | Призначення |
|---|---|
| Python | Backend |
| Aiogram | Telegram Bot |
| Redis | Cache |
| SQLite | Database |
| aiosqlite | Async SQL |
| aiohttp | HTTP requests |
| cryptography | Encryption |
| pandas | Analytics |
| matplotlib | Charts |

---

# 📦 Встановлення

## 1. Клонування проєкту

```bash
git clone <repository_url>
cd project
```

---

## 2. Створення virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

---

# ⚡ Встановлення Redis

## Docker

```bash
docker run -p 6379:6379 redis
```

---

## Перевірка Redis

```bash
redis-cli ping
```

Результат:

```text
PONG
```

---

# ⚙️ Налаштування `.env`

Створи `.env`

```env
BOT_TOKEN=your_bot_token

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

DICTIONARY_API=https://api.dictionaryapi.dev/api/v2/entries/en/
TRANSLATION_API=https://api.mymemory.translated.net/get

SECRET_KEY=your_fernet_key
```

---

# 🔑 Генерація SECRET_KEY

```python
from cryptography.fernet import Fernet

print(Fernet.generate_key().decode())
```

---

# ▶️ Запуск бота

```bash
python main.py
```

---

# 📌 Команди

| Команда | Опис |
|---|---|
| /start | Запуск бота |
| /help | Допомога |
| /stats | Статистика |
| /chart | Графік |

---

# 🗄 Структура бази даних

## Таблиця users

| Поле | Тип |
|---|---|
| id | INTEGER |
| telegram_id | TEXT |
| created_at | TEXT |

---

## Таблиця history

| Поле | Тип |
|---|---|
| id | INTEGER |
| user_id | TEXT |
| word | TEXT |
| translation | TEXT |
| created_at | TEXT |

---

# 🔥 SQL Queries

## CREATE TABLE

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE,
    created_at TEXT
)
```

---

## INSERT

```sql
INSERT INTO history (
    user_id,
    word,
    translation,
    created_at
)
VALUES (?, ?, ?, ?)
```

---

## SELECT

```sql
SELECT * FROM history
```

---

## COUNT

```sql
SELECT COUNT(*) FROM history
```

---

## ORDER BY

```sql
SELECT * FROM history
ORDER BY id DESC
```

---

## LIMIT

```sql
SELECT * FROM history
LIMIT 5
```

---

# 📁 Структура проєкту

```text
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
├── bot.db
└── README.md
```

---

# 🧠 Архітектура

```text
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
```

---

# 🔮 Можливі покращення

Можна додати:

- PostgreSQL
- Docker Compose
- Web Dashboard
- Admin Panel
- JWT Authentication
- Unit Tests
- CI/CD
- VPS Deploy
- Celery Tasks

---

# 👨‍💻 Автор

English Learning Telegram Bot

Async Python Backend Project
