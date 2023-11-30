from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, MessageHandler
from telegram.ext import filters
from config import API_TOKEN




async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


if __name__ == "__main__":
    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, hello))

    app.run_polling()
