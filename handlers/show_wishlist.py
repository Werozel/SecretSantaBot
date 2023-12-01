from telegram import Update
from telegram.ext import CommandHandler
from strings import START_PLAYER, NO_WISHLIST_YET, UNKNOWN_USER
from models.Player import Player
from globals import StateOfPlay


async def __show_wishlist(update: Update, _):
    player = StateOfPlay.get_player_by_id(update.effective_user.id)
    if player is None:
        await update.message.reply_text(UNKNOWN_USER)
        return

    wishlist = player.wishlist

    if wishlist is None or wishlist.isspace():
        await update.message.reply_text(NO_WISHLIST_YET)
        return

    await update.message.reply_text("Твой вишлист:")
    await update.message.reply_text(wishlist)


showWishlistHandler = CommandHandler("wishlist", __show_wishlist)
