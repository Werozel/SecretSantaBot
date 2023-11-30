from typing import Optional

from models.Player import Player
import json


class StateOfPlay:

    players: list[Player] = []

    @staticmethod
    def add_player(player: Player) -> None:
        StateOfPlay.players.append(player)

    @staticmethod
    def get_player_by_id(player_id: int) -> Optional[Player]:
        for player in StateOfPlay.players:
            if player.player_id == player_id:
                return player
        return None

    @staticmethod
    def to_string():
        return f"StateOfPlay: {StateOfPlay.players}"


    @staticmethod
    def save_to_json():
        obj = list(
            map(
                lambda x: x.to_json(),
                StateOfPlay.players,
            )
        )
        with open('data.json', 'w') as f:
            json.dump(obj, f)


