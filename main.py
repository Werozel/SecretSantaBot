from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, MessageHandler
from telegram.ext import filters
from config import API_TOKEN
from handlers.start_player import startPlayerHandler
from globals import StateOfPlay


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def checkState(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(StateOfPlay.to_string())

async def dumpGame(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    StateOfPlay.save_to_json()
    await update.message.reply_text("Готово")


if __name__ == "__main__":
    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(startPlayerHandler)
    app.add_handler(CommandHandler("check", checkState))
    app.add_handler(CommandHandler("dump", dumpGame))
    app.add_handler(MessageHandler(filters.TEXT, hello))

    app.run_polling()
