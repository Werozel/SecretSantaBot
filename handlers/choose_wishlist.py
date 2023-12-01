from telegram import Update

from globals import StateOfPlay
from models.Player import Player, PlayerStateEnum
from strings import WISHLIST_SELECTED, ANEKI, WISHLIST_SET_TOO_EARLY

import random


async def choose_wishlist(update: Update, player: Player):
    new_wishlist = update.message.text
    current_state = player.state
    if current_state == PlayerStateEnum.CHOOSING_WISHLIST:
        new_state = PlayerStateEnum.WAITING_FOR_START
    elif current_state == PlayerStateEnum.SELECTING_NICKNAME:
        await update.message.reply_text(WISHLIST_SET_TOO_EARLY)
        return
    else:
        new_state = current_state

    player.set_wishlist(new_wishlist, new_state)
    StateOfPlay.save_to_json()
    await update.message.reply_text(WISHLIST_SELECTED)
    await update.message.reply_text(random.choice(ANEKI))

