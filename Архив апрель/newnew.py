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
        # Convert audio to desired format with ffmpeg
        subprocess.run(['ffmpeg', '-i', f'downloaded_audios/{video_id}.mp3', '-vn', f'downloaded_audios/{video_id}_converted.mp3'], check=True)
        # Send the converted audio file to telegram group
        with open(f'downloaded_audios/{video_id}_converted.mp3', 'rb') as file:
            file_data = {'audio': file}
            response = requests.post('https://api.telegram.org/bot<BOT_TOKEN>/sendAudio', files=file_data)
            response_dict = json.loads(response.text)
        if response_dict['ok']:
            print(f"{video_id}_converted.mp3 was sent to the group")
        else:
            print(f"Error while sending {video_id}_converted.mp3 to the group: {response_dict['description']}")
    except subprocess.CalledProcessError as error:
        print(f"Error while processing playlist: {error}")

if __name__ == '__main__':
    os.makedirs('downloaded_audios', exist_ok=True)
    playlist_url = input("Enter the playlist URL: ")
    download_playlist(playlist_url)