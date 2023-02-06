import os
import youtube_dl
import requests
import telegram
from telegram import InputFile
import asyncio

download_folder = "downloaded_audios"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': download_folder + '/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

BOT_TOKEN = "5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k"
GROUP_CHAT_ID = "-1001874282744"
TOKEN = BOT_TOKEN
CHAT_ID = GROUP_CHAT_ID

def send_to_telegram(file_path):
    bot = telegram.Bot(token=TOKEN)
    bot.send_document(chat_id=CHAT_ID, document=InputFile(file_path))

playlist_url = input("Enter the URL of the YouTube playlist: ")
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(playlist_url, download=False)
    videos = info['entries']
    for video in videos:
        title = video['title'] + '.mp3'
        file_path = os.path.join(download_folder, title)
        if os.path.isfile(file_path):
            print("File already exists, skipping download: " + title)
            continue
        ydl.download([video['webpage_url']])
        send_to_telegram(file_path)
