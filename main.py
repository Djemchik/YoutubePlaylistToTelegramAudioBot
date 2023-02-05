import os
import requests
import youtube_dl

def download_playlist(playlist_url):
    ydl_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        ydl.download([playlist_url])

playlist_url = "<playlist url>"

current_directory = os.getcwd()
os.chdir(current_directory)

download_playlist(playlist_url)

def send_file(file_path, chat_id, token):
    file = {'document': (os.path.basename(file_path), open(file_path, 'rb'))}
    data = {'chat_id': chat_id}
    response = requests.post(f'https://api.telegram.org/bot{token}/sendDocument', data=data, files=file)
    return response.json()

current_directory = os.getcwd()
files = [f for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f))]

chat_id = "<chat id>"
token = "<telegram bot api token>"

for file in files:
    file_path = os.path.join(current_directory, file)
    send_file(file_path, chat_id, token)
