from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder
from config import API_TOKEN, ADMIN_ID
from handlers.genetic_text_message_handler import genericTextMessageHandler
from handlers.start_player import startPlayerHandler
from handlers.show_wishlist import showWishlistHandler
from handlers.show_players import showPlayersHandler
from globals import StateOfPlay


async def checkState(update: Update, _) -> None:
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text(StateOfPlay.to_string())


async def dumpGame(update: Update, _) -> None:
    if update.effective_user.id != ADMIN_ID:
        return
    StateOfPlay.save_to_json()
    await update.message.reply_text("Готово")


async def loadGame(update: Update, _) -> None:
    if update.effective_user.id != ADMIN_ID:
        return
    StateOfPlay.load_from_json()
    await update.message.reply_text("Готово")


async def clearGame(update: Update, _) -> None:
    if update.effective_user.id != ADMIN_ID:
        return
    StateOfPlay.players.clear()
    await update.message.reply_text("Готово")


if __name__ == "__main__":
    try:
        StateOfPlay.load_from_json()
    except:
        pass
    app = ApplicationBuilder().token(API_TOKEN).build()

    # TODO: @Werozel admin commands
    app.add_handler(CommandHandler("check", checkState))
    app.add_handler(CommandHandler("dump", dumpGame))
    app.add_handler(CommandHandler("load", loadGame))
    app.add_handler(CommandHandler("clear", clearGame))

    # Player commands
    app.add_handler(startPlayerHandler)
    app.add_handler(showWishlistHandler)
    app.add_handler(showPlayersHandler)
    app.add_handler(genericTextMessageHandler)

    app.run_polling()
