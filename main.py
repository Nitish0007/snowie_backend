from telegram.ext import Application, MessageHandler, filters
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers import handle_input

def main():
    print("Starting bot...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    print("Bot started")
    app.add_handler(MessageHandler(filters.TEXT, handle_input))
    print("Input handler 'handle_input' added")
    app.run_polling()
    print("Bot is running...")

if __name__ == "__main__":
    main()