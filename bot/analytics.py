import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

class Analytics:
    def __init__(self, db):
        self.db = db

    async def stats(self):
        data = await self.db.get_all()

        if not data:
            return "No data"

        df = pd.DataFrame(data)

        top = df["word"].value_counts().head(5)

        return (
            f"📊 Stats\n"
            f"Words: {len(df)}\n"
            f"Users: {df['user_id'].nunique()}\n\n"
            + "\n".join([f"{k}: {v}" for k, v in top.items()])
        )

    async def chart(self):
        data = await self.db.get_all()

        if not data:
            return None

        df = pd.DataFrame(data)
        top = df["word"].value_counts().head(5)

        plt.figure()
        top.plot(kind="bar")
        plt.tight_layout()

        path = "chart.png"
        plt.savefig(path)
        plt.close()

        return path