from telegram import Update

from globals import StateOfPlay
from models.Player import Player
from strings import NICK_SELECTED, INCORRECT_NICKNAME

from config import DIMAS_ID


async def select_nickname(update: Update, player: Player):
    nickname: str = update.message.text
    if nickname.isspace() or nickname.startswith("/"):
        await update.message.reply_text(INCORRECT_NICKNAME)
        return

    if player.player_id == DIMAS_ID:
        if "убийца" in nickname.lower():
            await update.message.reply_text("Всегда знал что ты убийца, не подвел (да, это пасхалка)")
        elif "легенд" in nickname.lower():
            await update.message.reply_text("Кажется фара теперь второй из легенд (да, это пасхалка)")
        else:
            await update.message.reply_text("Подводишь димас, подводишь")

    player.set_nickname(nickname)
    StateOfPlay.save_to_json()
    await update.message.reply_text(NICK_SELECTED(nickname))
