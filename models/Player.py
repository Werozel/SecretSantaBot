from enum import Enum


class StateEnum(Enum):
    UNREGISTERED = 0
    SELECTING_NICKNAME = 1
    CHOOSING_WISHLIST = 2
    WAITING_FOR_START = 3
    ASSIGNED_TARGET = 4
    ENDED_GAME = 5


class Player:

    player_id: str
    actual_name: str
    nickname: str
    wishlist: str
    target_player_id: str

    state: StateEnum

    def __str__(self):
        return f"{self.player_id}: {self.nickname}({self.actual_name})"
