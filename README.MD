```markdown
# Telegram RSS Bot (deploy trên Render)

Bot sẽ:
- Lưu subscribers (chat_id) vào SQLite (bot.db).
- Gửi tối đa 3 bài mới nhất chưa gửi trước đó mỗi giờ (không gửi trùng).
- Hỗ trợ /start để đăng ký và /stop để hủy đăng ký.
- Dùng aiosqlite để thao tác SQLite bất đồng bộ.

Files:
- bot.py
- requirements.txt
- Procfile

Cách deploy trên Render:
1. Tạo repository GitHub chứa các files trên.
2. Đăng nhập vào Render.com → New Web Service → Connect GitHub repo.
3. Chọn branch main.
4. Thêm Environment Variable:
   - BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
5. Build & Deploy. Render sẽ cài Python + packages và chạy `python3 bot.py` theo Procfile.
6. Lần đầu mở bot trên Telegram, gửi /start để bot lưu CHAT_ID.
7. Muốn ngừng nhận tin, gửi /stop.

Ghi chú:
- DB (bot.db) sẽ lưu trong thư mục làm việc của ứng dụng trên Render. Nếu bạn redeploy/scale, đảm bảo persistent storage hoặc thay bằng một DB bên ngoài nếu cần lưu lâu dài.
```
