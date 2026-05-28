import aiosqlite
from datetime import datetime

from censorship import is_censored


class Database:
    def __init__(
        self,
        security,
        db_path="bot.db"
    ):

        self.db_path = db_path
        self.security = security

    # ================= INIT =================
    async def init(self):

        async with aiosqlite.connect(
            self.db_path
        ) as db:

            # ---------- USERS ----------
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id TEXT UNIQUE,
                    created_at TEXT
                )
            """)

            # ---------- HISTORY ----------
            await db.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    word TEXT,
                    translation TEXT,
                    created_at TEXT
                )
            """)

            await db.commit()

            print("✅ Database initialized")

    # ================= ADD USER =================
    async def add_user(
        self,
        telegram_id
    ):

        encrypted_id = self.security.encrypt(
            str(telegram_id)
        )

        async with aiosqlite.connect(
            self.db_path
        ) as db:

            await db.execute("""
                INSERT OR IGNORE INTO users (
                    telegram_id,
                    created_at
                )
                VALUES (?, ?)
            """, (
                encrypted_id,
                datetime.now().isoformat()
            ))

            await db.commit()

    # ================= LOG WORD =================
    async def log_word(
        self,
        user_id,
        word,
        translation
    ):

        encrypted_user = self.security.encrypt(
            str(user_id)
        )

        encrypted_word = self.security.encrypt(
            word
        )

        encrypted_translation = self.security.encrypt(
            translation
        )

        async with aiosqlite.connect(
            self.db_path
        ) as db:

            await db.execute("""
                INSERT INTO history (
                    user_id,
                    word,
                    translation,
                    created_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                encrypted_user,
                encrypted_word,
                encrypted_translation,
                datetime.now().isoformat()
            ))

            await db.commit()

    # ================= GET ALL WORDS =================
    async def get_all_words(self):

        async with aiosqlite.connect(
            self.db_path
        ) as db:

            cursor = await db.execute("""
                SELECT word
                FROM history
            """)

            rows = await cursor.fetchall()

        words = []

        for row in rows:

            decrypted = self.security.decrypt(
                row[0]
            )

            if not is_censored(decrypted):
                words.append(decrypted)

        return words

    # ================= TOTAL WORDS =================
    async def total_words(self):

        async with aiosqlite.connect(
            self.db_path
        ) as db:

            cursor = await db.execute("""
                SELECT COUNT(*)
                FROM history
            """)

            result = await cursor.fetchone()

        return result[0]

    # ================= TOTAL USERS =================
    async def total_users(self):

        async with aiosqlite.connect(
            self.db_path
        ) as db:

            cursor = await db.execute("""
                SELECT COUNT(*)
                FROM users
            """)

            result = await cursor.fetchone()

        return result[0]

    # ================= LAST SEARCHES =================
    async def last_searches(
        self,
        limit=5
    ):

        async with aiosqlite.connect(
            self.db_path
        ) as db:

            cursor = await db.execute("""
                SELECT word, created_at
                FROM history
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))

            rows = await cursor.fetchall()

        result = []

        for row in rows:

            decrypted = self.security.decrypt(row[0])

            if not is_censored(decrypted):
                result.append({
                    "word": decrypted,
                    "created_at": row[1]
                })

        return result

    # ================= TOP WORDS =================
    async def top_words(
        self,
        limit=5
    ):

        async with aiosqlite.connect(
            self.db_path
        ) as db:

            cursor = await db.execute("""
                SELECT word
                FROM history
            """)

            rows = await cursor.fetchall()

        words = []

        for row in rows:

            decrypted = self.security.decrypt(
                row[0]
            )

            if not is_censored(decrypted):
                words.append(decrypted)

        stats = {}

        for word in words:

            stats[word] = stats.get(word, 0) + 1

        sorted_words = sorted(
            stats.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_words[:limit]