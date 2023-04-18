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
    'ignoreerrors': True, 
    'continue_dl': True
}

BOT_TOKEN = "5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k"
GROUP_CHAT_ID = "-1001874282744"
TOKEN = BOT_TOKEN
CHAT_ID = GROUP_CHAT_ID
bot = telegram.Bot(token=TOKEN)
chat_id = CHAT_ID
def send_audios_to_telegram(audios_folder):
    # Get the list of audio files in the audios_folder
    audio_files = [f for f in os.listdir(audios_folder) if f.endswith('.mp3')]

    for audio_file in audio_files:
        file_path = os.path.join(audios_folder, audio_file)
        bot.send_audio(chat_id=chat_id, audio=InputFile(file_path))

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
        
