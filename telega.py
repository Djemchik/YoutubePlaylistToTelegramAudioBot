
import os
import telegram

# Replace <token> with your Telegram Bot API token
bot = telegram.Bot(token='5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k')

# Replace <chat_id> with the chat ID of the Telegram group
chat_id = 8951433844

# Get the list of all MP3 files in the current directory
mp3_files = [f for f in os.listdir() if f.endswith('.mp3')]

for mp3_file in mp3_files:
    with open(mp3_file, 'rb') as f:
        bot.send_audio(chat_id=chat_id, audio=f, caption=mp3_file)
