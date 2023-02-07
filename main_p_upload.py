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
    }],	
    'ignoreerrors': True,
    'continue_dl': True
}


# URL of the YouTube playlist
playlist_url = input("Enter the URL of the YouTube playlist: ")

# Download the playlist using youtube_dl
async def download_playlist():
    # Download the playlist using youtube_dl
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        for entry in info_dict.get("entries", []):
            file_path = os.path.join(directory, entry["title"] + ".mp3")
            if os.path.exists(file_path):
                print(f"File '{entry['title']}' already exists, skipping download")
                continue
            try: 
                ydl.download([entry["webpage_url"]])
            except Exception as e:
                with open('failed_downloads.txt', 'a') as file:
                    file.write(f"{url} failed with error: {str(e)}\n")

async def send_music_files():
    # List of allowed file extensions for music files
    allowed_extensions = ['.mp3', '.flac', '.wav', '.m4a']

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        extension = os.path.splitext(filename)[1]

            # Send the file with a timeout of 5 seconds
        await asyncio.sleep(5)
        await bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))

async def main():
    await asyncio.gather(await download_playlist(), await send_music_files())
    print("Files have been successfully sent to the Telegram group")
asyncio.run(main())
