from telegram import Update
from telegram.ext import MessageHandler, filters
from strings import NOT_ALLOWED_MESSAGE, UNKNOWN_USER
from globals import StateOfPlay
from models.Player import PlayerStateEnum
from handlers.select_nickname import select_nickname
from handlers.choose_wishlist import choose_wishlist


async def __generic_text_message(update: Update, _):
    player_id = update.effective_user.id
    player = StateOfPlay.get_player_by_id(player_id)
    if player is None:
        await update.message.reply_text(UNKNOWN_USER)
        return

    message = update.message.text
    if message.startswith("/"):
        await update.message.reply_text(NOT_ALLOWED_MESSAGE)
        return

    if player.state == PlayerStateEnum.SELECTING_NICKNAME:
        await select_nickname(update, player)
    elif player.state == PlayerStateEnum.CHOOSING_WISHLIST:
        await choose_wishlist(update, player)
    elif player.state == PlayerStateEnum.WAITING_FOR_START:
        pass
    elif player.state == PlayerStateEnum.ASSIGNED_TARGET:
        pass
    elif player.state == PlayerStateEnum.ENDED_GAME:
        pass


genericTextMessageHandler = MessageHandler(filters.TEXT, __generic_text_message)