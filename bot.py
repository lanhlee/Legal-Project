#!/usr/bin/env python3
import os
import asyncio
import logging
from typing import List
import feedparser
import aiosqlite
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Cấu hình logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token bot (Render sẽ dùng biến môi trường này)
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    logger.error("BOT_TOKEN chưa được đặt. Thiết lập biến môi trường BOT_TOKEN và thử lại.")
    raise SystemExit("Missing BOT_TOKEN environment variable")

# Tên file DB SQLite
DB_FILE = "bot.db"

# RSS feed
FEED_URL = "https://vnexpress.net/rss/tin-moi-nhat.rss"

# Số bài gửi mỗi lần
MAX_ITEMS_PER_RUN = 3


async def init_db():
    """Khởi tạo DB nếu chưa có"""
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS subscribers (
                chat_id INTEGER PRIMARY KEY
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS sent_links (
                link TEXT PRIMARY KEY,
                title TEXT,
                published TEXT
            )
            """
        )
        await db.commit()
    logger.info("DB initialized")


# Subscriber helpers
async def add_subscriber(chat_id: int):
    async with aiosqlite.connect(DB_FILE) as db:
        try:
            await db.execute(
                "INSERT OR IGNORE INTO subscribers (chat_id) VALUES (?)", (chat_id,)
            )
            await db.commit()
            logger.info("Added subscriber %s", chat_id)
        except Exception:
            logger.exception("Failed to add subscriber %s", chat_id)


async def remove_subscriber(chat_id: int) -> bool:
    async with aiosqlite.connect(DB_FILE) as db:
        cur = await db.execute(
            "DELETE FROM subscribers WHERE chat_id = ?", (chat_id,)
        )
        await db.commit()
        removed = cur.rowcount if hasattr(cur, "rowcount") else None
        if removed:
            logger.info("Removed subscriber %s", chat_id)
        else:
            logger.info("Subscriber %s not found", chat_id)
        # Some aiosqlite versions don't populate rowcount; return True if no more exists
        return True


async def list_subscribers() -> List[int]:
    async with aiosqlite.connect(DB_FILE) as db:
        cur = await db.execute("SELECT chat_id FROM subscribers")
        rows = await cur.fetchall()
        return [row[0] for row in rows]


# Sent links helpers
async def get_existing_links(links: List[str]) -> set:
    if not links:
        return set()
    placeholders = ",".join("?" for _ in links)
    query = f"SELECT link FROM sent_links WHERE link IN ({placeholders})"
    async with aiosqlite.connect(DB_FILE) as db:
        cur = await db.execute(query, links)
        rows = await cur.fetchall()
        return {row[0] for row in rows}


async def mark_links_sent(entries: List[dict]):
    if not entries:
        return
    async with aiosqlite.connect(DB_FILE) as db:
        for e in entries:
            link = e.get("link", "")
            title = e.get("title", "")
            published = e.get("published", "")
            try:
                await db.execute(
                    "INSERT OR IGNORE INTO sent_links (link, title, published) VALUES (?, ?, ?)",
                    (link, title, published),
                )
            except Exception:
                logger.exception("Error marking link sent: %s", link)
        await db.commit()


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await add_subscriber(chat_id)
    await update.message.reply_text(
        "Xin chào! Bot đã lưu chat ID của bạn. Bot sẽ tự động gửi tin tức mới mỗi giờ.\n"
        "Nếu muốn dừng nhận tin, gửi /stop."
    )


# /stop command
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await remove_subscriber(chat_id)
    await update.message.reply_text("Bạn đã hủy đăng ký. Bot sẽ không gửi tin nữa cho chat này.")


# Gửi tin tức từ RSS feed (job callback)
async def send_news(context: ContextTypes.DEFAULT_TYPE):
    try:
        subscribers = await list_subscribers()
        if not subscribers:
            logger.info("Chưa có subscriber nào, bỏ qua lần gửi.")
            return

        feed = feedparser.parse(FEED_URL)
        entries = feed.entries or []
        if not entries:
            logger.info("RSS feed không có entries.")
            return

        # Lấy N đầu tiên (mới nhất). Sau đó lọc những link chưa gửi
        # Chuẩn bị list of links to check
        top_candidates = entries[:20]  # kiểm tra tối đa 20 gần nhất để tìm 3 chưa gửi
        candidate_links = [e.get("link", "") for e in top_candidates if e.get("link")]
        existing = await get_existing_links(candidate_links)

        # Chọn những entry chưa có trong sent_links, giữ thứ tự mới->cũ
        unseen = [e for e in top_candidates if e.get("link") and e.get("link") not in existing]
        if not unseen:
            logger.info("Không có tin mới chưa gửi.")
            return

        # Chọn tối đa MAX_ITEMS_PER_RUN (lấy 3 mới nhất), gửi theo thứ tự từ cũ -> mới để đọc thuận
        to_send = unseen[:MAX_ITEMS_PER_RUN]
        to_send.reverse()  # gửi từ cũ nhất trong số những mục mới để người dùng đọc theo thứ tự

        for entry in to_send:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            published = entry.get("published", "").strip() if entry.get("published") else ""
            message = f"{title}\n{link}"
            if published:
                message = f"{published}\n{message}"

            for cid in subscribers:
                try:
                    await context.bot.send_message(chat_id=cid, text=message)
                    logger.info("Đã gửi tới %s: %s", cid, link)
                except Exception:
                    logger.exception("Không gửi được tới %s", cid)

        # Đánh dấu đã gửi
        await mark_links_sent(to_send)

    except Exception:
        logger.exception("Lỗi trong send_news")


# Tạo app Telegram và đăng ký handler
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))


async def main():
    await init_db()
    # Đăng ký job gửi tin mỗi giờ (3600s). first=10 sẽ gửi lần đầu sau 10s khởi động (thử nghiệm).
    app.job_queue.run_repeating(send_news, interval=3600, first=10)
    logger.info("Bot đang chạy 24/7...")
    await app.run_polling()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot dừng.")
