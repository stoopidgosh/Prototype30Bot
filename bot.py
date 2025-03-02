import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7381143939:AAHZBCttdabsjydzS-AjxUfC_LxNEdCqBM4"
DOWNLOAD_PATH = "downloads/"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Kirim link video atau file untuk didownload.")

async def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    await update.message.reply_text("Sedang mengunduh...")
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_PATH}%(title)s.%(ext)s',
        'format': 'best'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
    with open(filename, 'rb') as video:
        await update.message.reply_video(video)
    
    os.remove(filename)  # Hapus setelah dikirim

async def download_file(update: Update, context: CallbackContext):
    file = await update.message.document.get_file()
    file_path = os.path.join(DOWNLOAD_PATH, update.message.document.file_name)
    
    await file.download(file_path)
    await update.message.reply_text(f"File disimpan: {file_path}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
app.add_handler(MessageHandler(filters.Document.ALL, download_file))

print("Bot berjalan...")
app.run_polling()
