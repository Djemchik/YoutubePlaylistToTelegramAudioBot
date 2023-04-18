import os
import subprocess
import requests
import json

def download_audio(video_url, audio_filename):
    try:
        subprocess.run(['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '-o', f'downloaded_audios/{audio_filename}.%(ext)s', video_url], check=True)
        print(f"Track {audio_filename} was successfully downloaded")
    except subprocess.CalledProcessError as error:
        print(f"Error while downloading {audio_filename}: {error}")

def download_playlist(playlist_url):
    try:
        result = subprocess.run(['youtube-dl', '--flat-playlist', '--get-id', playlist_url], capture_output=True, text=True)
        video_ids = result.stdout.strip().split('\n')
        with open('list_url.txt', 'a') as f:
            for video_id in video_ids:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                f.write(video_url + '\n')
                download_audio(video_url, video_id)
                send_to_telegram(f"downloaded_audios/{audio_filename}.mp3")
    except subprocess.CalledProcessError as error:
        print(f"Error while processing playlist: {error}")

def send_to_telegram(file_path):
    bot_token = "5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k"
    group_chat_id = "-1001874282744"
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    files = {'document': (file_path, open(file_path, 'rb'))}
    data = {'chat_id': group_chat_id}
    response = requests.post(url, data=data, files=files)
    result = json.loads(response.text)
    if result['ok']:
        print(f"File {file_path} was sent to the group")
    else:
        print(f"Error while sending {file_path} to the group: {result['description']}")

if __name__ == '__main__':
    os.makedirs('downloaded_audios', exist_ok=True)
    playlist_url = input("Enter the playlist URL: ")
    download_playlist(playlist_url)
