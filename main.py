import os
import threading
import cloudscraper
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask

# Flask app to keep the web service alive
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    web_app.run(host="0.0.0.0", port=5000)

# Get bot token, API ID, and API hash from environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Create the Pyrogram bot client
app = Client("gplink_bypass_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# /start command handler
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_name = message.from_user.first_name
    await message.reply(f"Hey {user_name} 👋, send me a gplink and I'll bypass it for you! 🚀")

# Handle incoming gplink.io and gplinks.co links
@app.on_message(filters.regex(r"(gplink\.io|gplinks\.co)/"))
async def handle_gplink(client, message: Message):
    gplink = message.text
    scraper = cloudscraper.create_scraper()

    try:
        final_url = scraper.get(gplink).url
        await message.reply(f"✅ Done! The bypassed link is: {final_url}")
    except Exception as e:
        await message.reply(f"❌ Error while bypassing: {e}")

if __name__ == "__main__":
    # Start Flask in a separate thread
    threading.Thread(target=run_flask).start()
    # Run the Telegram bot
    app.run()
