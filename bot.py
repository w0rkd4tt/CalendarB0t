import os
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 🛠 Cấu hình Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = "credentials.json"  # Đặt đúng tên tệp OAuth Client ID
TOKEN_FILE = "token.json"

# 📲 Cấu hình Telegram Bot
TELEGRAM_TOKEN = "8153267546:AAEykSI7lgg_0dCs_mElB8mia_fXYUZoA_g"  # Thay bằng token bot của bạn
CHAT_ID = "1106225659"  # Thay bằng ID Telegram của bạn

def send_telegram_message(message):
    """Gửi tin nhắn đến Telegram Bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}

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

def list_google_calendars():
    """Lấy danh sách lịch từ Google Calendar và gửi tới Telegram."""
    service = get_google_calendar_service()
    if not service:
        send_telegram_message("❌ Lỗi kết nối Google Calendar API.")
        return

    try:
        calendar_list = service.calendarList().list().execute()
        if "items" in calendar_list and calendar_list["items"]:
            message = "📅 *Danh sách Google Calendars:*\n"
            for calendar in calendar_list["items"]:
                message += f"- {calendar['summary']} (ID: `{calendar['id']}`)\n"
        else:
            message = "❌ Không tìm thấy lịch nào."

        send_telegram_message(message)

    except Exception as e:
        print(f"❌ Lỗi khi lấy danh sách lịch: {e}")
        send_telegram_message("❌ Đã xảy ra lỗi khi lấy lịch.")

if __name__ == "__main__":
    list_google_calendars()
