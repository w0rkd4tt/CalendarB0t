import os
import requests
import datetime
import asyncio
import schedule
import time
import threading
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram import Update, Bot

# 🛠 Cấu hình Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

# 📲 Cấu hình Telegram Bot
TELEGRAM_TOKEN = "8153267546:AAEykSI7lgg_0dCs_mElB8mia_fXYUZoA_g"  # Thay bằng token bot của bạn
CHAT_ID = "1106225659"

bot = Bot(token=TELEGRAM_TOKEN)
import datetime
import asyncio

# 🗓️ Lịch trình nhắc nhở sự kiện
def remind_upcoming_events():
    """Kiểm tra và gửi nhắc nhở cho sự kiện sắp diễn ra."""
    now = datetime.datetime.now(datetime.UTC)
    time_threshold = now + datetime.timedelta(minutes=30)  # Nhắc trước 30 phút

    upcoming_events = []
    for event in get_events(now, time_threshold):  # Lấy sự kiện trong 30 phút tới
        event_time = datetime.datetime.fromisoformat(event["start"])
        if now <= event_time <= time_threshold:
            upcoming_events.append(event)

    if upcoming_events:
        message = "⏳ *Sự kiện sắp diễn ra:*\n\n"
        for event in upcoming_events:
            message += f"✅ [{event['type']}] *{event['name']}*  \n🕒 {event['formatted_time']}  ({event['calendar_icon']})\n\n"
        send_telegram_message(message)


def send_telegram_message(message):
    """Gửi tin nhắn đến Telegram Bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi gửi tin nhắn Telegram: {e}")
        return None

def get_google_calendar_service():
    """Xác thực và kết nối với Google Calendar API."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        except Exception as e:
            print(f"❌ Lỗi xác thực Google API: {e}")
            return None

    return build("calendar", "v3", credentials=creds)

def get_events_from_all_calendars(time_min, time_max):
    """Lấy danh sách sự kiện từ tất cả lịch Google Calendar, sắp xếp theo ngày và phân loại theo icon."""
    service = get_google_calendar_service()
    if not service:
        return "❌ Không thể kết nối Google Calendar."

    try:
        # Lấy danh sách tất cả các lịch
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get("items", [])

        if not calendars:
            return "📭 Không tìm thấy lịch nào."

        # Tạo dictionary ánh xạ Calendar ID → Tên lịch & icon
        calendar_icons = {
                            "datnguyenlequoc2001@gmail.com": "🏢 Work",
                            "4a5bf44924705f9ce0c933c9816e708b1a649dfb48bc78b8d3c5e84b5c62b18b@group.calendar.google.com": "💬 CHAT3P",
                            "classroom101366239478702515619@group.calendar.google.com": "🎓 MMUD_ACT",
                            "vi.vietnamese#holiday@group.v.calendar.google.com": "🇻🇳 Ngày lễ VN",
                            "3e7b81ea36e2998b560f51928488307a8e32bc32d35c05c451dcc9e7da0de115@group.calendar.google.com": "📚 Study",
                            "c00863d8bf22ee5d92d80547f35e2c6a32282b5d58830cd7130a896ee1a4113b@group.calendar.google.com": "🎊 Event"
                        }


        all_events = []

        for calendar in calendars:
            calendar_id = calendar["id"]
            calendar_name = calendar.get("summary", "Unknown Calendar")
            calendar_icon = calendar_icons.get(calendar_id, "🗂 " + calendar_name)  # Mặc định nếu không có

            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min.isoformat() + "Z",
                timeMax=time_max.isoformat() + "Z",
                maxResults=100,  # Lấy tối đa 100 sự kiện
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            events = events_result.get("items", [])
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))[:10]  # Lấy YYYY-MM-DD
                formatted_date = datetime.datetime.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")  # Format DD/MM/YYYY
                event_type = event.get("description", "Event")  # Nếu có mô tả, dùng nó làm loại sự kiện

                all_events.append({
                    "name": event["summary"],
                    "date": start,
                    "formatted_date": formatted_date,
                    "type": event_type,
                    "calendar_icon": calendar_icon
                })

        if not all_events:
            return "📭 Không có sự kiện nào."

        # Sắp xếp sự kiện theo ngày tháng
        all_events.sort(key=lambda e: e["date"])

        # Format danh sách sự kiện theo yêu cầu
        message = "📅 *DANH SÁCH SỰ KIỆN:*\n\n"
        for event in all_events:
            emoji = "✅" if event["type"].lower() == "event" else "📖"
            message += f"{emoji} [{event['type']}] *{event['name']}*  \n🗓 {event['formatted_date']}  ({event['calendar_icon']})\n\n"
        message += "📭 Không có sự kiện nào." if not all_events else ""


        return message
    except Exception as e:
        print(f"❌ Lỗi khi lấy sự kiện: {e}")
        return "❌ Đã xảy ra lỗi khi lấy lịch."




async def check_today(update: Update, context: CallbackContext):
    now = datetime.datetime.now(datetime.UTC)
    time_min = datetime.datetime.combine(now.date(), datetime.time.min)
    time_max = datetime.datetime.combine(now.date(), datetime.time.max)

    message = get_events_from_all_calendars(time_min, time_max)
    await update.message.reply_text(message, parse_mode="Markdown")


async def check_week(update: Update, context: CallbackContext):
    """Lấy danh sách sự kiện từ tất cả lịch trong 7 ngày tới và sắp xếp theo ngày."""
    now = datetime.datetime.now(datetime.UTC)
    time_min = datetime.datetime.combine(now.date(), datetime.time.min)
    time_max = time_min + datetime.timedelta(days=7)

    message = get_events_from_all_calendars(time_min, time_max)
    await update.message.reply_text(message, parse_mode="Markdown")


def remind_events():
    """Tự động nhắc nhở sự kiện lúc 9h sáng và 9h tối."""
    now = datetime.datetime.now(datetime.UTC)

    time_min = datetime.datetime.combine(now.date(), datetime.time.min)
    time_max = datetime.datetime.combine(now.date(), datetime.time.max)
    message = get_events(time_min, time_max)

    if "📭 Không có sự kiện nào." not in message:
        send_telegram_message("⏰ *Nhắc nhở sự kiện hôm nay:*\n" + message)

# 🕘 Lên lịch nhắc nhở mỗi ngày vào 9h sáng và 9h tối
schedule.every().day.at("09:00").do(remind_events)
schedule.every().day.at("21:00").do(remind_events)

def run_scheduler():
    """Chạy lịch nhắc nhở trong nền."""
    while True:
        schedule.run_pending()
        time.sleep(60)

async def scheduled_reminders():
    """Chạy kiểm tra sự kiện mỗi 5 phút."""
    while True:
        remind_upcoming_events()
        await asyncio.sleep(300)  # 300 giây = 5 phút

def main():
    """Khởi chạy bot Telegram."""
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("check", check_today))
    app.add_handler(CommandHandler("checkweek", check_week))

    # Chạy scheduler trong một luồng riêng
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Chạy bot Telegram
    app.run_polling()

    # Chạy nhắc nhở tự động
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_reminders())
    loop.run_forever()

if __name__ == "__main__":
    main()


