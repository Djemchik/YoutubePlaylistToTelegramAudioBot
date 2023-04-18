import asyncio
import os
import telegram
import youtube_dl

# Replace with your own bot token
bot = telegram.Bot(token="5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k")

# Replace with the chat_id of the group you want to send the files to
chat_id = -1001874282744

# Directory where your audio files are stored
directory = 'downloaded_audios'

# Options for youtube_dl
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded_audios/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


# URL of the YouTube playlist
playlist_url = input("Enter the URL of the YouTube playlist: ")
# Download the playlist using youtube_dl
async def download_playlist():
    # Download the playlist using youtube_dl
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for info in ydl.extract_info(playlist_url, download=True):
        # Append the title of the file to the list of downloaded files
        downloaded_files.append(info['title'])
        return downloaded_files

async def send_music_files():
    # List of allowed file extensions for music files
    allowed_extensions = ['.mp3', '.flac', '.wav', '.m4a']

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        extension = os.path.splitext(filename)[1]

        # Check if the file has an allowed extension
        if extension in allowed_extensions:
            await bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
        # Add a delay of 5 seconds to avoid triggering the flood protection
        await asyncio.sleep(5)
async def main():
    await asyncio.gather(download_playlist(), send_music_files())

asyncio.run(main())
