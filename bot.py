import json
import datetime
import schedule
import time
import os
import requests
from telegram import Bot

# Lấy biến môi trường từ Railway
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GOOGLE_SHEETS_API = os.getenv("GOOGLE_SHEETS_API")  # URL API Google Sheets

bot = Bot(token=TOKEN)

# Lấy danh sách nhân viên từ Google Sheets
def load_birthdays():
    response = requests.get(GOOGLE_SHEETS_API)
    return response.json()

# Gửi tin nhắn chúc mừng kèm ảnh
def check_and_send_birthday_message():
    today = datetime.datetime.now().strftime("%d-%m")
    birthdays = load_birthdays()

    for person in birthdays:
        if person["dob"] == today:
            message = f"🎉 Chúc mừng sinh nhật {person['name']}! 🎂🥳\nChúc bạn một ngày thật vui vẻ và hạnh phúc! 🎁🎊"
            
            # Gửi ảnh kèm tin nhắn
            bot.send_photo(chat_id=CHAT_ID, photo=person["photo"], caption=message)

# Lên lịch chạy hàng ngày lúc 8h sáng
schedule.every().day.at("08:00").do(check_and_send_birthday_message)

while True:
    schedule.run_pending()
    time.sleep(60)
