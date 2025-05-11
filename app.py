import os
import cloudscraper
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

scraper = cloudscraper.create_scraper()  # Cloudscraper instance

# Function to start the bot and greet the user
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f"Hey {user.first_name}👋, send me a gplink and I'll bypass it for you! 🌐🔗\n\nJust send the link and I'll handle the rest! 🚀"
    )

# Function to detect and bypass the gplink
def handle_message(update: Update, context: CallbackContext) -> None:
    message = update.message.text

    if "gplink" in message:  # Detect gplink URL
        try:
            # Bypass the link using cloudscraper
            final_link = scraper.get(message).url
            update.message.reply_text(
                f"🚀 Link Bypassed! Here is your final destination link:\n{final_link} 🔗"
            )
        except Exception as e:
            update.message.reply_text(
                f"❌ Failed to bypass the link. Please try again later.\nError: {str(e)}"
            )
    else:
        update.message.reply_text(
            "I can only bypass gplinks. Please send me a valid gplink link."
        )

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Handle /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Handle any incoming message
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you send a signal (CTRL+C)
    updater.idle()

if __name__ == '__main__':
    main()
  
