import os
import youtube_dl
import requests

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

def send_audio_to_telegram(audio_file_path):
	audio_filename = os.path.basename(audio_file_path)
	audio = open(audio_file_path, 'rb')
	files = {'audio': (audio_filename, audio)}
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
        file_path = os.path.join(download_folder, title)
        if os.path.isfile(file_path):
            print("File already exists, skipping download: " + title)
            send_audio_to_telegram(file_path)
            continue
        ydl.download([video['webpage_url']])
        send_audio_to_telegram(file_path)
