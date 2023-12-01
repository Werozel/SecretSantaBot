from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from strings import GAME_STOPPED, GAME_ENDED
from models.Player import Player, PlayerStateEnum
from globals import StateOfPlay
from config import ADMIN_ID, GAME_ADMIN_ID


async def __end_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_id = update.effective_user.id
    if player_id not in [ADMIN_ID, GAME_ADMIN_ID]:
        return

    for player in StateOfPlay.players.values():
        player.end_game()
    StateOfPlay.save_to_json()

    await update.message.reply_text(GAME_STOPPED)
    for player in StateOfPlay.players.values():
        await context.bot.send_message(player.player_id, GAME_ENDED)

endGameHandler = CommandHandler("end_game", __end_game)
