import os
import cloudscraper
from pyrogram import Client, filters
from pyrogram.types import Message

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

# Handle incoming links and bypass them using cloudscraper
@app.on_message(filters.regex(r"(gplink\.io|gplinks\.co)/"))
async def handle_gplink(client, message: Message):
    gplink = message.text
    scraper = cloudscraper.create_scraper()

    try:
        # Bypass the gplink and get the final URL
        final_url = scraper.get(gplink).url
        await message.reply(f"✅ Done! The bypassed link is: {final_url}")
    except Exception as e:
        await message.reply(f"❌ Error while bypassing: {e}")

# Run the bot
if __name__ == "__main__":
    app.run()
