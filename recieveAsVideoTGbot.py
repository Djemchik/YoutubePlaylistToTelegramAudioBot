from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import subprocess

TOKEN = '5261340309:AAHnAdbOBJ7V4gUhk-HcU6zbtDrIXP_RiCM'

def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я бот, который может отправлять видео.')

def encode_video(update: Update, context):
    video_file = context.bot.getFile(update.message.video.file_id)
    file_name = os.path.basename(video_file.file_path)
    temp_file_path = f'temp/{file_name}'
    video_file.download(temp_file_path)
    out_file_path = f'temp/{os.path.splitext(file_name)[0]}.mp4'
    cmd = f'ffmpeg -i "{temp_file_path}" -c:v libx264 -c:a copy "{out_file_path}"'
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            percent = get_progress(output)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Прогресс: {percent}%')
    context.bot.send_video(chat_id=update.effective_chat.id, video=open(out_file_path, 'rb'))

def get_progress(output):
    """
    Получает процент выполнения команды FFmpeg из строки вывода.

    :param output: строка вывода из процесса FFmpeg.
    :return: процент выполнения команды.
    """
    if "Duration" in output:
        duration = output.split("Duration: ")[1].split(",")[0]
        h, m, s = duration.split(":")
        total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
    if "time=" in output:
        time = output.split("time=")[1].split(" ")[0]
        h, m, s = time.split(":")
        current_seconds = int(h) * 3600 + int(m) * 60 + float(s)
        percent = round(current_seconds / total_seconds * 100)
        return percent
    return None

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.video & (Filters.mime_type("video/avi") | Filters.mime_type("video/x-matroska")), encode_video))
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
