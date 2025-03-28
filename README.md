# CalendarB0t 📅🤖

`CalendarB0t` là một Telegram bot được tích hợp với Google Calendar API để quản lý và nhắc nhở các sự kiện. Bot hỗ trợ kiểm tra sự kiện trong ngày, trong tuần, và tự động gửi thông báo nhắc nhở các sự kiện sắp diễn ra.

## 🛠 Tính năng

1. **Kiểm tra sự kiện trong ngày**:
   - Lệnh: `/check`
   - Hiển thị danh sách các sự kiện trong ngày từ tất cả các lịch Google Calendar được kết nối.

2. **Kiểm tra sự kiện trong tuần**:
   - Lệnh: `/checkweek`
   - Hiển thị danh sách các sự kiện trong 7 ngày tới từ tất cả các lịch Google Calendar.

3. **Nhắc nhở sự kiện tự động**:
   - Bot tự động gửi thông báo nhắc nhở các sự kiện trong ngày vào lúc:
     - 9:00 sáng
     - 9:00 tối
   - Nhắc nhở các sự kiện sắp diễn ra trước 30 phút.

4. **Hỗ trợ nhiều lịch Google Calendar**:
   - Bot lấy sự kiện từ tất cả các lịch được liên kết với tài khoản Google của bạn.
   - Các lịch được phân loại bằng biểu tượng (icon) để dễ nhận biết.

## 🚀 Cách sử dụng

### 1. Cài đặt môi trường
- Cài đặt các thư viện cần thiết:
```bash
  pip install python-telegram-bot google-auth google-auth-oauthlib google-api-python-client schedule
```
### 2. Cấu hình Google Calendar API

Tạo một dự án trên `Google Cloud Console`.
Kích hoạt Google Calendar API.
Tải xuống tệp `credentials.json` và đặt nó trong thư mục dự án.

### 3. Cấu hình Telegram Bot
Tạo một bot trên `BotFather` và lấy `TELEGRAM_TOKEN`.
Cập nhật `TELEGRAM_TOKEN` và `CHAT_ID` trong tệp `bot_v2.py`.
### 4. Chạy bot
Chạy bot bằng lệnh:

```
python3 bot_v2.py
```

### 5. Sử dụng bot trên Telegram
Gửi các lệnh sau đến bot:

- `/check`: Kiểm tra sự kiện trong ngày.
- `/checkweek`: Kiểm tra sự kiện trong tuần.

## 📋 Function được sử dụng

- get_google_calendar_service(): Xác thực và kết nối với Google Calendar API.
- get_events_from_all_calendars(time_min, time_max): Lấy danh sách sự kiện từ tất cả các lịch trong khoảng thời gian chỉ định.
- check_today(): Xử lý lệnh /check để kiểm tra sự kiện trong ngày.
- check_week(): Xử lý lệnh /checkweek để kiểm tra sự kiện trong tuần.
- remind_events(): Tự động nhắc nhở sự kiện vào 9:00 sáng và 9:00 tối.
- remind_upcoming_events(): Nhắc nhở các sự kiện sắp diễn ra trước 30 phút.

🕒 Lịch trình tự động
- 9:00 sáng: Nhắc nhở sự kiện trong ngày.
- 9:00 tối: Nhắc nhở sự kiện trong ngày.
- Mỗi 5 phút: Kiểm tra và nhắc nhở các sự kiện sắp diễn ra.

### 📌 Lưu ý
Đảm bảo tệp credentials.json và token.json được đặt đúng vị trí trong thư mục dự án.
Bot cần quyền truy cập vào Google Calendar của bạn. Hãy đảm bảo bạn đã cấp quyền khi chạy lần đầu.

### 📧 Author - w0rkkd4t