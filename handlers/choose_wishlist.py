from telegram import Update
from telegram.ext import ContextTypes

from globals import StateOfPlay
from models.Player import Player, PlayerStateEnum
from strings import WISHLIST_SELECTED, ANEKI, WISHLIST_SET_TOO_EARLY, TARGET_WISHLIST_CHANGED, CANCEL_WISHLIST_EDITING

import random


async def choose_wishlist(update: Update, player: Player, context: ContextTypes.DEFAULT_TYPE):
    new_wishlist = update.message.text

    if new_wishlist.lower().strip() == "отмена":
        await update.message.reply_text(CANCEL_WISHLIST_EDITING)
        if player.target_player_id is None:
            new_state = PlayerStateEnum.WAITING_FOR_START
        else:
            new_state = PlayerStateEnum.ASSIGNED_TARGET
        player.state = new_state
        StateOfPlay.save_to_json()
        return

    current_state = player.state

    if current_state == PlayerStateEnum.CHOOSING_WISHLIST:
        if player.target_player_id is None:
            new_state = PlayerStateEnum.WAITING_FOR_START
        else:
            new_state = PlayerStateEnum.ASSIGNED_TARGET
    elif current_state == PlayerStateEnum.SELECTING_NICKNAME:
        await update.message.reply_text(WISHLIST_SET_TOO_EARLY)
        return
    else:
        new_state = current_state

    player.set_wishlist(new_wishlist, new_state)
    StateOfPlay.save_to_json()

    santa_player = StateOfPlay.get_santa_of_player(player.player_id)
    await context.bot.send_message(santa_player.player_id, TARGET_WISHLIST_CHANGED)
    await context.bot.send_message(santa_player.player_id, new_wishlist)

    await update.message.reply_text(WISHLIST_SELECTED)
    await update.message.reply_text(random.choice(ANEKI))

