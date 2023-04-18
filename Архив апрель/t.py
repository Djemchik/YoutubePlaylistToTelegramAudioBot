import os
import glob
import logging
from telegram import InputFile
from telegram import Bot

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Replace the token with the token of your bot.
bot = Bot(token='5640044198:AAFmq7K5uA7TtJaX2ku41cWdRjPXpRkAY6k')

# Replace the chat_id with the chat_id of your Telegram chat.
chat_id = -1001874282744

# Find all audio files in the current directory.
audio_files = glob.glob('*.mp3') + glob.glob('*.m4a') + glob.glob('*.ogg') + glob.glob('*.flac')

for audio_file in audio_files:
    try:
        bot.send_audio(chat_id=chat_id, audio=InputFile(audio_file))
    except Exception as e:
        logger.error(f'Error sending audio: {e}')
