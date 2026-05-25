import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


class Analytics:
    def __init__(self, db):

        self.db = db

    # ================= STATS =================
    async def stats(self):

        total_words = await self.db.total_words()

        total_users = await self.db.total_users()

        top_words = await self.db.top_words()

        last = await self.db.last_searches()

        text = (
            f"📊 <b>Статистика</b>\n\n"

            f"🔤 Слів: {total_words}\n"

            f"👤 Користувачів: {total_users}\n\n"

            f"🔥 <b>Топ слів:</b>\n"
        )

        for word, count in top_words:

            text += f"• {word} — {count}\n"

        text += "\n🕒 <b>Останні пошуки:</b>\n"

        for item in last:

            text += f"• {item['word']}\n"

        return text

    # ================= CHART =================
    async def chart(self):

        top_words = await self.db.top_words()

        if not top_words:
            return None

        words = [x[0] for x in top_words]

        counts = [x[1] for x in top_words]

        plt.figure(figsize=(8, 5))

        plt.bar(words, counts)

        plt.title("Top Words")

        plt.tight_layout()

        path = "chart.png"

        plt.savefig(path)

        plt.close()

        return path