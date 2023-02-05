import os
import requests
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

# specify the URL of the playlist
playlist_url = "https://www.youtube.com/playlist?list=PLOAFzRws139CoGX2UvsGx5yWplrxBB6Hh"

# download the audio files from the playlist
try:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])
except Exception as e:
    print(e)
    sys.exit(1)

def send_file(file_path, chat_id, token):
    file = {'document': (os.path.basename(file_path), open(file_path, 'rb'))}
    data = {'chat_id': chat_id}
    response = requests.post(f'https://api.telegram.org/bot{token}/sendDocument', data=data, files=file)
    return response.json()

current_directory = os.getcwd()
files = [f for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f))]

chat_id = "<-895143844>"
token = "<5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k>"

for file in files:
    file_path = os.path.join(current_directory, file)
    send_file(file_path, chat_id, token)
