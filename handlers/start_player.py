from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, MessageHandler
from telegram.ext import filters
from strings import START_PLAYER
from models.Player import Player
from globals import StateOfPlay


async def __startPlayer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_name = update.effective_user.first_name
    player_id = update.effective_user.id
    player = Player(player_id, player_name)
    StateOfPlay.add_player(player)
    await update.message.reply_text(START_PLAYER)


startPlayerHandler = CommandHandler("start", __startPlayer)
