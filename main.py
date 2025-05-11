import os
import time
import cloudscraper
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread

# Flask app to keep the web service alive
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    web_app.run(host="0.0.0.0", port=5000, use_reloader=False)  # `use_reloader=False` to avoid Flask re-running the script

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Create the Pyrogram bot client
app = Client("gplink_bypass_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Function to bypass the GPLinks URL
def bypass_gplinks(url: str) -> str:
    client = cloudscraper.create_scraper()

    initial = client.get(url)
    soup = BeautifulSoup(initial.content, "html.parser")
    
    try:
        inputs = soup.find("form", id="go-link").find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
    except Exception:
        return "Could not parse the bypass form."
    
    time.sleep(10)  # GPLinks requires a wait

    headers = {"x-requested-with": "XMLHttpRequest"}
    response = client.post("https://gplinks.co/links/go", data=data, headers=headers)
    
    try:
        return response.json()["url"]
    except:
        return "Bypass failed. GPLinks may have changed their structure."

# /start command handler
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_name = message.from_user.first_name
    await message.reply(f"Hey {user_name} 👋, send me a GPLinks URL and I'll bypass it for you! 🚀")

# Handle incoming GPLinks URL and bypass it
@app.on_message(filters.regex(r"(https?://)?(www\.)?(gplinks\.co|gplink\.io)/[^\s]+"))
async def handle_gplink(client, message: Message):
    gplink = message.text.strip()
    await message.reply("⏳ Bypassing your GPLink...")
    try:
        final_url = bypass_gplinks(gplink)
        await message.reply(f"✅ Done! The bypassed link is:\n{final_url}")
    except Exception as e:
        await message.reply(f"❌ Error while bypassing: {e}")

# Run the Flask app in a separate thread and the Pyrogram bot
if __name__ == "__main__":
    # Run Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run the Pyrogram bot
    app.run()
