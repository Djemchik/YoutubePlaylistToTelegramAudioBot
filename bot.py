import os
import requests
import asyncio
import youtube_dl
import telegram

BOT_TOKEN = "5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k"
TELEGRAM_BOT_TOKEN = BOT_TOKEN
GROUP_CHAT_ID = "-1001874282744"
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def send_audio_to_telegram(audio_file_path):
    filename = os.path.basename(audio_file_path)
    audio = open(audio_file_path, 'rb')
    files = {'audio': (filename, audio)}
    response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendAudio',
                             data={'chat_id': GROUP_CHAT_ID}, files=files)
    if response.status_code != 200:
        print("Failed to send audio to Telegram group: " + response.text)

def download_and_send_audio_files(playlist_url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        videos = info['entries']
        for video in videos:
            title = video['title'] + '.mp3'
            if os.path.isfile(title):
                print("File already exists, skipping download: " + title)
                send_audio_to_telegram(title)
                continue
            ydl.download([video['webpage_url']])
            send_audio_to_telegram(title)



async def main():
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    offset = 0
    while True:
        updates = await bot.get_updates(offset=offset)
        if not updates:
            continue
        for update in updates:
            message = update.message
            handle_message(message)
            offset = update.update_id + 1

async def handle_message(message):
    if message.text == '/start':
        bot.send_message(chat_id=message.chat.id, text="Welcome!")
    elif message.text.startswith('https://www.youtube.com/playlist?list='):
        playlist_url = message.text
        download_and_send_audio_files(playlist_url)
        bot.send_message(chat_id=message.chat.id, text="Downloading and sending the audio files...")
    else:
        bot.send_message(chat_id=message.chat.id, text="Invalid command. Please enter a valid YouTube playlist URL.")





asyncio.run(main())
