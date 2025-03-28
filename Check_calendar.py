import os
import datetime
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Phạm vi truy cập Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_google_calendar_service():
    creds = None
    # Kiểm tra nếu đã có token (đã đăng nhập trước đó)
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Nếu chưa có token hoặc token hết hạn, yêu cầu người dùng đăng nhập
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "token.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Lưu token để lần sau không cần đăng nhập lại
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Kết nối đến Google Calendar API
    service = build("calendar", "v3", credentials=creds)
    return service

def list_calendars():
    service = get_google_calendar_service()
    calendar_list = service.calendarList().list().execute()
    
    if "items" in calendar_list and len(calendar_list["items"]) > 0:
        print("✅ Your Calendars:")
        for calendar in calendar_list["items"]:
            print(f"- {calendar['summary']} (ID: {calendar['id']})")
    else:
        print("❌ No calendars found.")

if __name__ == "__main__":
    list_calendars()
