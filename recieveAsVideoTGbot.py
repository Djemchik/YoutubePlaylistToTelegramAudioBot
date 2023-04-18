import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '5261340309:AAHnAdbOBJ7V4gUhk-HcU6zbtDrIXP_RiCM'

def start(update: telegram.Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я бот, который может отправлять видео.')
    
def handle_video(update: telegram.Update, context: CallbackContext) -> None:
    message = update.message.reply_text('Видео загружается...')
    video_file = context.bot.getFile(update.message.video.file_id)
    video_file.download(custom_path='video.mp4', timeout=100)
    message.edit_text('Видео загружено, отправляем...')
    context.bot.send_video(chat_id=update.effective_chat.id, video=open('video.mp4', 'rb'))
    message.delete()
    os.remove('video.mp4')

def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.video, handle_video))
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
