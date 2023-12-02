from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from strings import GAME_STARTED, ASSIGN_PLAYER, EMPTY_WISHLIST
from models.Player import Player
from globals import StateOfPlay
from config import ADMIN_ID, GAME_ADMIN_ID
import random


async def __start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_id = update.effective_user.id
    if player_id not in [ADMIN_ID, GAME_ADMIN_ID]:
        return

    fe_player = StateOfPlay.get_player_by_username("ddaria_f")
    ma_player = StateOfPlay.get_player_by_username("wojiaomaliya")
    dr_player = StateOfPlay.get_player_by_username("warswefought")

    if fe_player and ma_player:
        fe_player.assign_target(ma_player.player_id)
    if ma_player and dr_player:
        ma_player.assign_target(dr_player.player_id)

    already_selected_player_ids = list(
        filter(
            lambda x: x,
            map(
                lambda player: player.target_player_id,
                StateOfPlay.players.values()
            )
        )
    )

    player_ids_to_select_from = list(
        map(
            lambda player: player.player_id,
            filter(
                lambda player: player.player_id not in already_selected_player_ids,
                StateOfPlay.players.values()
            )
        )
    )

    players_without_target = list(
        filter(
            lambda player: player.target_player_id is None,
            StateOfPlay.players.values()
        )
    )

    for player in players_without_target:
        target_player_id = player.player_id
        while ((target_player_id == player.player_id) or
               (player.username == "eugen_gurov" and target_player_id in [ADMIN_ID, GAME_ADMIN_ID]) or
               (player.player_id == ADMIN_ID and target_player_id == GAME_ADMIN_ID) or
               (player.player_id == GAME_ADMIN_ID and target_player_id == ADMIN_ID)
        ):
            target_player_id = random.choice(player_ids_to_select_from)
        player.assign_target(target_player_id)
        player_ids_to_select_from.remove(target_player_id)

    StateOfPlay.save_to_json()
    await update.message.reply_text(GAME_STARTED)

    for player in StateOfPlay.players.values():
        target_player = StateOfPlay.get_player_by_id(player.target_player_id)
        await context.bot.send_message(player.player_id, ASSIGN_PLAYER(str(target_player)))
        if target_player.wishlist:
            await context.bot.send_message(player.player_id, target_player.wishlist)
        else:
            await context.bot.send_message(player.player_id, EMPTY_WISHLIST)


startGameHandler = CommandHandler("start_game", __start_game)
