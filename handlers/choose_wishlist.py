from telegram import Update

from globals import StateOfPlay
from models.Player import Player
from strings import WISHLIST_SELECTED, ANEKI

import random


async def choose_wishlist(update: Update, player: Player):
    wishlist = update.message.text

    player.set_wishlist(wishlist)
    StateOfPlay.save_to_json()
    await update.message.reply_text(WISHLIST_SELECTED)
    await update.message.reply_text(random.choice(ANEKI))

