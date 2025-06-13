import os
import telebot
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Telegram Bot Token (Get from @BotFather)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

# Google Drive & YouTube APIs Setup
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/youtube.upload']
SERVICE_ACCOUNT_FILE = 'service_account.json'  # Google Cloud Service Account Key

# YouTube Upload Function
def upload_to_youtube(file_path, title="Uploaded from Drive"):
    youtube = build('youtube', 'v3', credentials=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES))
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "Uploaded via Telegram Bot"
            },
            "status": {
                "privacyStatus": "private"  # Change to "public" if needed
            }
        },
        media_body=MediaFileUpload(file_path)
    )
    response = request.execute()
    return response

# /start Command - Welcome Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
    🎉 **Welcome to Your YouTube Uploader Bot!** 🎉

    **How to Use:**
    1. Send a Google Drive link with `/upload <Drive-Link>`.
    2. The bot will download & upload it to YouTube.

    Example:
    `/upload https://drive.google.com/file/d/123abc/view`

    ❓ Need help? Contact @YourUsername
    """
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# /upload Command - Handle Drive to YouTube Upload
@bot.message_handler(commands=['upload'])
def handle_upload(message):
    try:
        drive_link = message.text.split()[1]  # Extract Drive Link
        bot.reply_to(message, "⏳ Downloading from Google Drive...")
        
        # (Add code to download from Drive using Drive API)
        file_path = "downloaded_video.mp4"
        
        bot.reply_to(message, "⏳ Uploading to YouTube...")
        upload_to_youtube(file_path)
        bot.reply_to(message, "✅ **Video uploaded to YouTube successfully!**", parse_mode="Markdown")
    
    except IndexError:
        bot.reply_to(message, "❌ **Error:** Please provide a Google Drive link.\nExample: `/upload https://drive.google.com/...`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ **Error:** {str(e)}")

bot.polling()
