import os
import subprocess

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
    except subprocess.CalledProcessError as error:
        print(f"Error while processing playlist: {error}")

if __name__ == '__main__':
    os.makedirs('downloaded_audios', exist_ok=True)
    playlist_url = input("Enter the playlist URL: ")
    download_playlist(playlist_url)
