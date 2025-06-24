import os
import time
import re
import requests
from bs4 import BeautifulSoup
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = os.getenv("URL")

DATE_PATTERN = re.compile(r'\b\d{1,2}\.\d{1,2}(\.\d{4})?\b')

def check_for_dates():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            dates_found = DATE_PATTERN.findall(text)
            return bool(dates_found)
    except Exception as e:
        print("Error:", e)
    return False

def run():
    bot = Bot(token=TOKEN)
    notified = False
    while True:
        if check_for_dates():
            if not notified:
                bot.send_message(chat_id=CHAT_ID, text="🟢 Термин появился! Проверь сайт МВД.")
                notified = True
        else:
            notified = False
        time.sleep(300)

if __name__ == "__main__":
    run()