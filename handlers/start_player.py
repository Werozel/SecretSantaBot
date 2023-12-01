from telegram import Update
from telegram.ext import CommandHandler
from strings import START_PLAYER, ALREADY_STARTED
from models.Player import Player
from globals import StateOfPlay


async def __start_player(update: Update, _):
    player_name = update.effective_user.first_name
    player_id = update.effective_user.id
    if StateOfPlay.get_player_by_id(player_id) is not None:
        await update.message.reply_text(ALREADY_STARTED)
        return

    player = Player(player_id, player_name)
    StateOfPlay.add_player(player)
    StateOfPlay.save_to_json()
    await update.message.reply_text(START_PLAYER)


startPlayerHandler = CommandHandler("start", __start_player)
