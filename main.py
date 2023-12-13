import random

from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes

from config import API_TOKEN, ADMIN_ID, GAME_ADMIN_ID
from globals import StateOfPlay
from handlers.end_game_handler import endGameHandler
from handlers.genetic_text_message_handler import genericTextMessageHandler
from handlers.select_nickname import select_nickname
from handlers.show_players import showPlayersHandler
from handlers.show_wishlist import showWishlistHandler
from handlers.start_game_handler import startGameHandler
from handlers.start_player import startPlayerHandler
from models.Player import PlayerStateEnum
from strings import UNKNOWN_USER, WISHLIST_SET_TOO_EARLY, SELECT_WISHLIST, WISHLIST_WILL_BE_SENT_TO_SANTA, ANEKI, REQUESTED_NEW_WISHLIST, REQUEST_TO_UPDATE_WISHLIST


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


async def show_status(update: Update, _):
    current_user_id = update.effective_user.id
    if current_user_id not in [ADMIN_ID, GAME_ADMIN_ID]:
        return
    text = ""
    for player in StateOfPlay.players.values():
        text += f"{str(player)} - {player.state.value}\n"

    if current_user_id == ADMIN_ID:
        text += "\n"

        for player in StateOfPlay.players.values():
            # TODO: @Werozel handle None
            target_player = StateOfPlay.get_player_by_id(player.target_player_id)
            text += f"{str(player)} -> {str(target_player)}\n"

    await update.message.reply_text(text)


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in [ADMIN_ID, GAME_ADMIN_ID]:
        return

    ids = list(
        map(
            lambda x: x.player_id,
            StateOfPlay.players.values()
        )
    )

    for player_id in ids:
        await context.bot.send_message(player_id, " ".join(context.args))


async def change_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = StateOfPlay.get_player_by_id(update.effective_user.id)
    if player is None:
        await update.message.reply_text(UNKNOWN_USER)
        return

    await select_nickname(update, player, " ".join(context.args))


async def change_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = StateOfPlay.get_player_by_id(update.effective_user.id)
    if player is None:
        await update.message.reply_text(UNKNOWN_USER)
        return

    current_state = player.state
    if current_state == PlayerStateEnum.SELECTING_NICKNAME:
        await update.message.reply_text(WISHLIST_SET_TOO_EARLY)
        return
    elif current_state == PlayerStateEnum.ASSIGNED_TARGET:
        await update.message.reply_text(WISHLIST_WILL_BE_SENT_TO_SANTA)
        player.state = PlayerStateEnum.CHOOSING_WISHLIST
    else:
        player.state = PlayerStateEnum.CHOOSING_WISHLIST
        await update.message.reply_text(SELECT_WISHLIST)


async def send_anek(update: Update, _):
    await update.message.reply_text(random.choice(ANEKI))


async def request_another_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = StateOfPlay.get_player_by_id(update.effective_user.id)
    if player is None:
        await update.message.reply_text(UNKNOWN_USER)
        return

    target_player = StateOfPlay.get_player_by_id(player.target_player_id)
    if target_player is None:
        await update.message.reply_text("Кажется тебе некому дарить подарок, это странно, напиши @KhGleb")
        return
    await update.message.reply_text(REQUESTED_NEW_WISHLIST(target_player.nickname))
    await context.bot.send_message(target_player.player_id, REQUEST_TO_UPDATE_WISHLIST)


if __name__ == "__main__":
    try:
        StateOfPlay.load_from_json()
    except:
        pass
    app = ApplicationBuilder().token(API_TOKEN).build()

    # Аdmin commands
    app.add_handler(CommandHandler("check", checkState))
    app.add_handler(CommandHandler("dump", dumpGame))
    app.add_handler(CommandHandler("load", loadGame))
    app.add_handler(CommandHandler("clear", clearGame))

    # Game admin commands
    app.add_handler(startGameHandler)
    app.add_handler(endGameHandler)
    app.add_handler(CommandHandler("status", show_status))
    app.add_handler(CommandHandler("broadcast", broadcast))

    # Player commands
    app.add_handler(CommandHandler("anek", send_anek))
    app.add_handler(CommandHandler("change_nickname", change_nickname))
    app.add_handler(CommandHandler("change_wishlist", change_wishlist))
    app.add_handler(CommandHandler("santa_stuck", request_another_wishlist))
    app.add_handler(startPlayerHandler)
    app.add_handler(showWishlistHandler)
    app.add_handler(showPlayersHandler)
    app.add_handler(genericTextMessageHandler)

    app.run_polling()
