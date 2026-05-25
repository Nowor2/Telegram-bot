from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Handlers:
    def __init__(
        self,
        dp,
        cache,
        db,
        dict_svc,
        trans_svc,
        analytics,
        security,
        config
    ):

        self.dp = dp
        self.cache = cache
        self.db = db
        self.dict = dict_svc
        self.trans = trans_svc
        self.analytics = analytics
        self.security = security
        self.config = config

        self.register()

    # ================= REGISTER =================
    def register(self):
        self.dp.message(CommandStart())(
            self.start
        )

        self.dp.message(Command("help"))(
            self.help
        )

        self.dp.message(Command("stats"))(
            self.stats
        )

        self.dp.message(Command("chart"))(
            self.chart
        )

        self.dp.message(
            F.text & ~F.text.startswith("/")
        )(
            self.word
        )

        self.dp.callback_query(
            F.data.startswith("refresh:")
        )(
            self.refresh
        )

        self.dp.callback_query(
            F.data.startswith("clear:")
        )(
            self.clear
        )

    # ================= KEYBOARD =================
    def keyboard(self, word):
        builder = InlineKeyboardBuilder()

        builder.button(
            text="🔄 Refresh",
            callback_data=f"refresh:{word}"
        )

        builder.button(
            text="🗑 Clear Cache",
            callback_data=f"clear:{word}"
        )

        builder.adjust(2)

        return builder.as_markup()

    # ================= START =================
    async def start(self, m: Message):

        await self.db.add_user(
    m.from_user.id
        )

        text = (
            "👋 <b>Welcome to English Learning Bot</b>\n\n"

            "📘 Надішли будь-яке англійське слово,\n"
            "і я покажу:\n\n"

            "🇺🇦 Переклад\n"
            "🔊 Транскрипцію\n"
            "📚 Частину мови\n"
            "📖 Значення слова\n"
            "✏️ Приклад використання\n\n"

            "⚡ Redis Cache\n"
            "🗄 SQLite Database\n"
            "🔐 Encryption + Hashing\n\n"

            "📌 Команди:\n"
            "/help\n"
            "/stats\n"
            "/chart"
        )

        await m.answer(
            text,
            parse_mode="HTML"
        )

    # ================= HELP =================
    async def help(self, m: Message):

        text = (
            "📚 <b>Доступні команди</b>\n\n"

            "/start — запуск бота\n"
            "/help — допомога\n"
            "/stats — статистика\n"
            "/chart — графік популярних слів\n\n"

            "🔍 Просто напиши слово.\n\n"

            "Наприклад:\n"
            "<code>apple</code>"
        )

        await m.answer(
            text,
            parse_mode="HTML"
        )

    # ================= FORMAT WORD =================
    def format_word(
        self,
        word,
        translation,
        data,
        source
    ):

        try:
            phonetic = data[0].get(
                "phonetic",
                "N/A"
            )

            meanings = data[0].get(
                "meanings",
                []
            )

            if not meanings:
                return "❌ No meanings found"

            meaning = meanings[0]

            part_of_speech = meaning.get(
                "partOfSpeech",
                "N/A"
            )

            definitions = meaning.get(
                "definitions",
                []
            )

            if not definitions:
                return "❌ No definitions found"

            definition = definitions[0].get(
                "definition",
                "No definition"
            )

            example = definitions[0].get(
                "example",
                "No example"
            )

            text = (
                f"{source}\n\n"

                f"📘 <b>Word:</b>\n"
                f"{word.capitalize()}\n\n"

                f"🇺🇦 <b>Translation:</b>\n"
                f"{translation}\n\n"

                f"🔊 <b>Phonetic:</b>\n"
                f"{phonetic}\n\n"

                f"📚 <b>Part of Speech:</b>\n"
                f"{part_of_speech}\n\n"

                f"📖 <b>Definition:</b>\n"
                f"{definition}\n\n"

                f"✏️ <b>Example:</b>\n"
                f"{example}"
            )

            return text

        except Exception as e:
            print("FORMAT ERROR:", e)

            return "❌ Parse error"

    # ================= WORD =================
    async def word(self, m: Message):

        await self.db.log_word(
    m.from_user.id,
    word,
    translation
        )

        word = m.text.lower().strip()

        hashed = self.security.hash_text(
            word
        )

        key = f"word:{hashed}"

        # ---------- CACHE ----------
        cached = await self.cache.get(key)

        if cached:

            print("✅ CACHE HIT")

            data = cached["dictionary"]

            translation = cached["translation"]

            source = "⚡ <b>From Cache</b>"

        else:

            print("❌ CACHE MISS")

            data = await self.dict.get(word)

            if not data:
                await m.answer(
                    "❌ Word not found"
                )
                return

            translation = await self.trans.translate(
                word
            )

            await self.cache.set(
                key,
                {
                    "dictionary": data,
                    "translation": translation
                },
                self.config.CACHE_TTL
            )

            print("💾 CACHE SAVED")

            source = "🌐 <b>From API</b>"

        # ---------- DATABASE ----------
        await self.db.log_word(
            m.from_user.id,
            word,
            translation
        )

        # ---------- FORMAT ----------
        text = self.format_word(
            word,
            translation,
            data,
            source
        )

        # ---------- SEND ----------
        await m.answer(
            text,
            parse_mode="HTML",
            reply_markup=self.keyboard(word)
        )

    # ================= REFRESH =================
    async def refresh(
        self,
        call: CallbackQuery
    ):

        word = call.data.split(":")[1]

        hashed = self.security.hash_text(
            word
        )

        data = await self.dict.get(word)

        if not data:
            await call.answer(
                "❌ Error"
            )
            return

        translation = await self.trans.translate(
            word
        )

        await self.cache.set(
            f"word:{hashed}",
            {
                "dictionary": data,
                "translation": translation
            },
            self.config.CACHE_TTL
        )

        text = self.format_word(
            word,
            translation,
            data,
            "🌐 <b>Updated from API</b>"
        )

        await call.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=self.keyboard(word)
        )

        await call.answer(
            "🔄 Updated"
        )

    # ================= CLEAR CACHE =================
    async def clear(
        self,
        call: CallbackQuery
    ):

        word = call.data.split(":")[1]

        hashed = self.security.hash_text(
            word
        )

        await self.cache.delete(
            f"word:{hashed}"
        )

        await call.answer(
            "🗑 Cache cleared"
        )

    # ================= STATS =================
    async def stats(self, m: Message):

        stats = await self.analytics.stats()

        await m.answer(stats)

    # ================= CHART =================
    async def chart(self, m: Message):

        path = await self.analytics.chart()

        if not path:
            await m.answer(
                "📭 No data yet"
            )
            return

        await m.answer_photo(
            FSInputFile(path)
        )