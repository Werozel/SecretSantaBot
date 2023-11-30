from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes
from config import API_TOKEN
from handlers.genetic_text_message_handler import genericTextMessage
from globals import StateOfPlay


async def checkState(update: Update, _) -> None:
    await update.message.reply_text(StateOfPlay.to_string())


async def dumpGame(update: Update, _) -> None:
    StateOfPlay.save_to_json()
    await update.message.reply_text("Готово")


async def loadGame(update: Update, _) -> None:
    StateOfPlay.load_from_json()
    await update.message.reply_text("Готово")


if __name__ == "__main__":
    # TODO: @Werozel uncomment
    # StateOfPlay.load_from_json()
    app = ApplicationBuilder().token(API_TOKEN).build()

    # TODO: @Werozel admin commands
    app.add_handler(CommandHandler("check", checkState))
    app.add_handler(CommandHandler("dump", dumpGame))
    app.add_handler(CommandHandler("load", loadGame))

    # Player commands
    app.add_handler(genericTextMessageHandler)

    app.run_polling()
