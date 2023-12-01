from telegram import Update
from telegram.ext import CommandHandler
from strings import NO_PLAYERS_YET
from models.Player import PlayerStateEnum
from globals import StateOfPlay


async def __show_players(update: Update, _):
    waiting_players = []
    for player in StateOfPlay.players.values():
        if (player.state == PlayerStateEnum.CHOOSING_WISHLIST or
                player.state == PlayerStateEnum.WAITING_FOR_START or
                player.state == PlayerStateEnum.ASSIGNED_TARGET):
            waiting_players.append(player)
    if not waiting_players:
        await update.message.reply_text(NO_PLAYERS_YET)
        return
    await update.message.reply_text("\n".join(map(lambda x: f"{x.nickname}(@{x.username})", waiting_players)))


showPlayersHandler = CommandHandler("players", __show_players)
