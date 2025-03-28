# Telegram Bot

## Giới thiệu
Đây là một Telegram bot được phát triển bằng Python sử dụng thư viện `python-telegram-bot`. Bot có thể xử lý tin nhắn, lệnh và nhắc nhở sự kiện tự động.

## Tính năng
- Tự động nhắc nhở các sự kiện vào **9h sáng** và **9h tối** mỗi ngày.
- Danh sách các sự kiện trong ngày và trong tuần.
- Xử lý lệnh cơ bản:
  - `/check` - Kiểm tra các task trong ngày.
  - `/listtasks` - Kiểm tra toàn bộ task trong tuần.
- Hỗ trợ API bên thứ ba để lấy dữ liệu (ví dụ: thời tiết, tin tức, v.v.).
- Lưu trữ và quản lý thông tin người dùng.

## Cài đặt
### 1. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_BOT_REPO.git
cd YOUR_BOT_REPO
```

### 2. Cài đặt môi trường và thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 3. Cấu hình Bot
Tạo file `.env` để lưu token bot:
```env
BOT_TOKEN=8153267546:AAFBgSr924OX3yR0yLrsFDtlqf5HRPCybaw
```

### 4. Chạy bot
```bash
python bot.py
```

## Cách sử dụng
- **Bắt đầu bot**: `/start`
- **Xem hướng dẫn**: `/help`
- **Kiểm tra các task trong ngày**: `/check`
- **Kiểm tra toàn bộ task trong tuần**: `/listtasks`
- **Nhắc nhở tự động**: Mỗi ngày vào **9h sáng** và **9h tối**, bot sẽ gửi danh sách các sự kiện trong ngày và trong tuần.

## Công nghệ sử dụng
- Python
- `python-telegram-bot`
- Docker (nếu cần triển khai container)

## Triển khai
Bot có thể triển khai trên:
- **Heroku**
- **VPS (Ubuntu, Debian, v.v.)**
- **Docker** (Chạy với `docker-compose`)

## Đóng góp
Nếu bạn muốn đóng góp cho dự án, hãy mở Pull Request hoặc Issue trên GitHub.

## Liên hệ
- **Tác giả**: YOUR_NAME
- **Email**: your_email@example.com
- **Telegram**: @your_username

---
Chúc bạn sử dụng bot vui vẻ! 🚀

