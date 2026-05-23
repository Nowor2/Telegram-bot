import aiosqlite
from datetime import datetime

class Database:
    def __init__(self, security, db_path="bot.db"):
        self.db_path = db_path
        self.security = security

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_id TEXT,
                    word TEXT,
                    translation TEXT
                )
            """)
            await db.commit()

    async def log(self, user_id, word, translation):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO history VALUES (NULL, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                self.security.encrypt(str(user_id)),
                self.security.encrypt(word),
                self.security.encrypt(translation),
            ))
            await db.commit()

    async def get_all(self):
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute("SELECT user_id, word, translation FROM history")
            rows = await cur.fetchall()

        result = []
        for r in rows:
            result.append({
                "user_id": self.security.decrypt(r[0]),
                "word": self.security.decrypt(r[1]),
                "translation": self.security.decrypt(r[2]),
            })
        return result