from enum import Enum
from typing import Optional
import json


class PlayerStateEnum(Enum):
    SELECTING_NICKNAME = "Selecting nickname"
    CHOOSING_WISHLIST = "Choosing wishlist"
    WAITING_FOR_START = "Waiting for start"
    ASSIGNED_TARGET = "Assigned another player"
    ENDED_GAME = "Game ended"


class Player:

    def __init__(
            self,
            player_id: int,
            actual_name: str,
            nickname: Optional[str] = None,
            wishlist: Optional[str] = None,
            target_player_id: Optional[int] = None,
            state: PlayerStateEnum = PlayerStateEnum.SELECTING_NICKNAME,
    ):
        self.player_id: int = player_id
        self.actual_name: str = actual_name
        self.nickname: Optional[str] = nickname
        self.wishlist: Optional[str] = wishlist
        self.target_player_id: Optional[int] = target_player_id

        self.state: PlayerStateEnum = state

    def set_nickname(
            self,
            nickname: str,
            state: PlayerStateEnum = PlayerStateEnum.CHOOSING_WISHLIST
    ) -> None:
        self.nickname = nickname
        self.state = state

    def set_wishlist(
            self,
            wishlist: str,
            state: PlayerStateEnum = PlayerStateEnum.WAITING_FOR_START
    ) -> None:
        self.wishlist = wishlist
        self.state = state

    def assign_target(
            self,
            target_player_id: int,
            state: PlayerStateEnum = PlayerStateEnum.ASSIGNED_TARGET
    ) -> None:
        self.target_player_id = target_player_id
        self.state = state

    def end_game(self):
        self.state = PlayerStateEnum.ENDED_GAME

    def __repr__(self):
        return f"{self.player_id}: {self.nickname}({self.actual_name})"

    def __str__(self):
        return f"{self.player_id}: {self.nickname}({self.actual_name})"

    def to_json(self) -> dict:
        return {
            "player_id": self.player_id,
            "actual_name": self.actual_name,
            "nickname": self.nickname,
            "wishlist": self.wishlist,
            "target_player_id": self.target_player_id,
            "state": self.state.value
        }

    @staticmethod
    def from_json(obj: dict) -> 'Player':
        return Player(
            obj["player_id"],
            obj["actual_name"],
            obj.get("nickname", None),
            obj.get("wishlist", None),
            obj.get("target_player_id", None),
            obj.get("state", None),
        )