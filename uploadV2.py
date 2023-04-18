import os
import telegram
import asyncio
import requests
import time

BOT_TOKEN = "5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k"

GROUP_CHAT_ID = "-1001874282744"
TOKEN = BOT_TOKEN
CHAT_ID = GROUP_CHAT_ID

async def get_all_chats():
    bot = telegram.Bot(token=TOKEN)
    updates = await bot.get_updates()
    for i, update in enumerate(updates):
        print(f"{i+1}. {update.message.chat.title if update.message.chat.type != 'private' else update.message.chat.username}")
    chat_num = int(input("Please enter the number of the chat you would like to upload files to: "))
    return updates[chat_num-1].message.chat_id

async def send_to_telegram(file_path, chat_id):
    bot = telegram.Bot(token=TOKEN)
    response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendAudio',
                             data={'chat_id': chat_id}, files={'audio': open(file_path, 'rb')})
    if response.status_code != 200:
        print("Failed to send audio to Telegram group: " + response.text)

def is_audio_file(file):
    return file.endswith('.mp3') or file.endswith('.wav') or file.endswith('.ogg')

def display_directories():
    directories = [d for d in os.listdir() if os.path.isdir(d)]
    for i, directory in enumerate(directories):
        print(f"{i+1}. {directory}")

display_directories()
selected_directory = int(input("Please enter the number of the directory you would like to upload files from: "))
directories = [d for d in os.listdir() if os.path.isdir(d)]
folder = directories[selected_directory - 1]

chat_id = asyncio.run(get_all_chats())

files = os.listdir(folder)
total_files = len(files)
processed_files = 0
start = time.time()
for file in files:
    if is_audio_file(file):
        file_path = os.path.join(folder, file)
        asyncio.run(send_to_telegram(file_path, chat_id))
        processed_files += 1
        time_elapsed = time.time() - start
        estimated_time_left = (time_elapsed / processed_files) * (total_files - processed_files)
        print(f"{processed_files} of {total_files} files processed. {file} sent. Estimated time left: {estimated_time_left:.2f} seconds")
        time.sleep(2)

