import os
import youtube_dl
import requests

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ignoreerrors': True,
    'continue_dl': True
}

BOT_TOKEN = "5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k"
GROUP_CHAT_ID = "8951433844"

def send_audio_to_telegram(audio_file_path):
    audio = open(audio_file_path, 'rb')
    files = {'audio': ('audio.mp3', audio)}
    response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendAudio',
                             data={'chat_id': GROUP_CHAT_ID}, files=files)
    if response.status_code != 200:
        print("Failed to send audio to Telegram group: " + response.text)

playlist_url = input("Enter the URL of the YouTube playlist: ")
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(playlist_url, download=False)
    videos = info['entries']
    for video in videos:
        title = video['title'] + '.mp3'
        if os.path.isfile(title):
            print("File already exists: " + title)
            continue
        ydl.download([video['webpage_url']])
