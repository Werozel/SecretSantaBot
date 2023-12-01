from telegram import Update

from globals import StateOfPlay
from models.Player import Player, PlayerStateEnum
from strings import NICK_SELECTED, INCORRECT_NICKNAME

from config import DIMAS_ID


async def select_nickname(update: Update, player: Player, new_nickname: str):
    if new_nickname.isspace() or new_nickname.startswith("/"):
        await update.message.reply_text(INCORRECT_NICKNAME)
        return

    if player.player_id == DIMAS_ID:
        if "убийца" in new_nickname.lower():
            await update.message.reply_text("Всегда знал что ты убийца, не подвел (да, это пасхалка)")
        elif "легенд" in new_nickname.lower():
            await update.message.reply_text("Кажется фара теперь второй из легенд (да, это пасхалка)")
        else:
            await update.message.reply_text("Подводишь димас, подводишь")

    current_state = player.state
    if current_state == PlayerStateEnum.SELECTING_NICKNAME:
        new_state = PlayerStateEnum.CHOOSING_WISHLIST
    else:
        new_state = current_state

    player.set_nickname(new_nickname, new_state)

    StateOfPlay.save_to_json()
    await update.message.reply_text(NICK_SELECTED(new_nickname))
