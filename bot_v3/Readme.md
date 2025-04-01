# Hướng Dẫn Triển Khai n8n Trên Fly.io và Kết Nối Google Calendar với Telegram

## 1. Triển Khai n8n Trên Fly.io
### 1.1. Cài Đặt Fly.io
Fly.io là một nền tảng chạy container serverless. Trước tiên, bạn cần cài đặt CLI của Fly:
```sh
curl -fsSL https://fly.io/install.sh | sh
```
Sau đó, đăng nhập vào Fly:
```sh
fly auth login
```

### 1.2. Triển khai n8n trên Fly.io
#### Bước 1: Tạo ứng dụng Fly
```sh
fly launch --name n8n-app
```
Chọn khu vực máy chủ gần bạn nhất và chờ Fly.io tạo cấu trúc ứng dụng.

#### Bước 2: Cấu hình biến môi trường
n8n cần một số biến môi trường để hoạt động đúng cách. Chạy lệnh sau để đặt biến môi trường:
```sh
fly secrets set N8N_BASIC_AUTH_USER=admin \
                N8N_BASIC_AUTH_PASSWORD=strongpassword \
                WEBHOOK_TUNNEL_URL=https://n8n-app.fly.dev/
```

#### Bước 3: Deploy ứng dụng
```sh
fly deploy
```
Sau khi hoàn thành, n8n sẽ chạy tại `https://n8n-app.fly.dev/`.

## 2. Google Apps Script để Gửi Thông Báo Sự Kiện
### 2.1. Tạo Apps Script
1. Truy cập [Google Apps Script](https://script.google.com/)
2. Tạo dự án mới và dán đoạn mã sau:

```javascript
function getAllEventsAndSendToTelegram() {
  const webhookUrl = 'https://n8n-app.fly.dev/webhook/telegram'; // Webhook của n8n
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const calendars = CalendarApp.getAllCalendars();
  let eventsData = [];

  calendars.forEach(calendar => {
    const events = calendar.getEvents(today, new Date(today.getTime() + 86400000));
    events.forEach(event => {
      eventsData.push({
        calendarName: calendar.getName(),
        eventTitle: event.getTitle(),
        eventStartTime: event.getStartTime().toISOString(),
        eventEndTime: event.getEndTime().toISOString(),
        eventLocation: event.getLocation() || 'Không có địa điểm',
        eventDescription: event.getDescription() || 'Không có mô tả'
      });
    });
  });

  eventsData.forEach(event => {
    const options = {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify(event)
    };
    UrlFetchApp.fetch(webhookUrl, options);
  });
}
```

3. **Lưu lại** và đặt lịch chạy bằng Triggers (VD: chạy hàng ngày vào 7h sáng).

## 3. Cấu Hình n8n Để Gửi Tin Nhắn Telegram
### 3.1. Tạo Workflow Trong n8n
1. **Tạo Webhook Trigger**:
   - Chọn **Webhook** node.
   - Chọn phương thức **POST**.
   - Copy URL Webhook (`https://n8n-app.fly.dev/webhook/telegram`).
   
2. **Thêm Node Xử Lý Dữ Liệu**:
   - Dùng node **Set** để format dữ liệu thành nội dung tin nhắn.

3. **Gửi Tin Nhắn Telegram**:
   - Thêm node **Telegram** (chế độ "Send Message").
   - Nhập `Chat ID` và `Bot Token`.
   - Format tin nhắn theo dạng:
     ```
     🗓 *Sự kiện mới!*
     📌 *Tên:* {{$json["eventTitle"]}}
     📍 *Địa điểm:* {{$json["eventLocation"]}}
     🕒 *Bắt đầu:* {{$json["eventStartTime"]}}
     🕓 *Kết thúc:* {{$json["eventEndTime"]}}
     📝 *Mô tả:* {{$json["eventDescription"]}}
     ```
   - Chạy thử workflow.

Sau khi hoàn thành, hệ thống sẽ tự động gửi thông báo sự kiện từ Google Calendar đến Telegram thông qua n8n trên Fly.io! 🚀



Author - w0rkkd4tt

