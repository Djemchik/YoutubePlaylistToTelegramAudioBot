import os
import telegram
from telegram import InputFile
import asyncio
import requests
import time

BOT_TOKEN = "5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k"
GROUP_CHAT_ID = "-1001874282744"
TOKEN = BOT_TOKEN
CHAT_ID = GROUP_CHAT_ID

def send_to_telegram(file_path):
    bot = telegram.Bot(token=TOKEN)
    response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendAudio',
                             data={'chat_id': GROUP_CHAT_ID}, files={'audio': open(file_path, 'rb')})
    if response.status_code != 200:
        print("Failed to send audio to Telegram group: " + response.text)

def is_audio_file(file):
    return file.endswith('.mp3') or file.endswith('.wav') or file.endswith('.ogg')

folder = "downloaded_audios"
files = os.listdir(folder)
total_files = len(files)
processed_files = 0
for file in files:
    if is_audio_file(file):
        file_path = os.path.join(folder, file)
        send_to_telegram(file_path)
        time.sleep(5)
        processed_files += 1
        print(f"Upload progress: {100 * processed_files / total_files:.2f}%")