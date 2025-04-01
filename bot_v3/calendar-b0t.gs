# App Script code for Google Calendar Bot
// Mô tả: Lấy tất cả các sự kiện trong ngày từ tất cả các lịch Google và gửi chúng tới một webhook.

// Hàm lấy tất cả các sự kiện trong ngày và sắp xếp theo thứ tự thời gian
function getAllEvents(targetDate) {
  const startOfDay = new Date(targetDate);
  startOfDay.setHours(0, 0, 0, 0);

  const endOfDay = new Date(targetDate);
  endOfDay.setHours(23, 59, 59, 999);

  const calendars = CalendarApp.getAllCalendars();
  let eventsData = [];

  calendars.forEach(function(calendar) {
    const events = calendar.getEvents(startOfDay, endOfDay);
    
    events.forEach(function(event) {
      eventsData.push({
        calendarName: calendar.getName(),
        eventTitle: event.getTitle(),
        eventStartTime: event.getStartTime(),
        eventEndTime: event.getEndTime(),
        eventLocation: event.getLocation() || "Không có địa điểm",
        eventDescription: event.getDescription() || "Không có mô tả"
      });
    });
  });

  // Sắp xếp sự kiện theo thời gian bắt đầu
  eventsData.sort((a, b) => new Date(a.eventStartTime) - new Date(b.eventStartTime));

  return eventsData;
}

// Hàm gửi từng sự kiện tới webhook
function sendToWebhook(eventsData) {
  const webhookUrl = 'https://my-n8n.fly.dev/webhook/calendar-b0t'; // Thay bằng URL webhook thật

  eventsData.forEach(function(event) {
    const payload = JSON.stringify({
      calendarName: event.calendarName,
      eventTitle: event.eventTitle,
      eventStartTime: event.eventStartTime.toISOString(),
      eventEndTime: event.eventEndTime.toISOString(),
      eventLocation: event.eventLocation,
      eventDescription: event.eventDescription
    });

    const options = {
      method: 'POST',
      contentType: 'application/json',
      payload: payload
    };

    UrlFetchApp.fetch(webhookUrl, options);
  });
}

// Hàm tổng hợp: lấy sự kiện và gửi đi
function processEventsAndSend() {
  const targetDate = new Date(); // Ngày hôm nay
  const eventsData = getAllEvents(targetDate);
  sendToWebhook(eventsData);
}
