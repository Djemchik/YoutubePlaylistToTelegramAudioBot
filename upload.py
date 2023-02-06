import os
import telegram
from telegram import InputFile
import asyncio
import requests

BOT_TOKEN = "5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k"
GROUP_CHAT_ID = "-1001874282744"
TOKEN = BOT_TOKEN
CHAT_ID = GROUP_CHAT_ID

def send_to_telegram(file_path):
    bot = telegram.Bot(token=TOKEN)
    response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendAudio',
                             data={'chat_id': GROUP_CHAT_ID}, files=folder)
    if response.status_code != 200:
        print("Failed to send audio to Telegram group: " + response.text)

folder = "downloaded_audios"
files = os.listdir(folder)
for file in files:
    file_path = os.path.join(folder, file)
    send_to_telegram(file_path)
