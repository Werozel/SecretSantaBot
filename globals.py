from typing import Optional

from models.Player import Player
import json


class StateOfPlay:

    players: dict[int, Player] = {}

    @staticmethod
    def add_player(player: Player) -> None:
        StateOfPlay.players.update({player.player_id: player})

    @staticmethod
    def get_player_by_id(player_id: int) -> Optional[Player]:
        return StateOfPlay.players.get(player_id, None)

    @staticmethod
    def to_string():
        return f"StateOfPlay: {StateOfPlay.players}"


    @staticmethod
    def save_to_json():
        obj = list(
            map(
                lambda x: x.to_json(),
                StateOfPlay.players.values(),
            )
        )
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_from_json():
        with open("data.json", "r", encoding='utf-8') as f:
            obj: list = json.load(f)
            players = list(
                map(
                    lambda x: Player.from_json(x),
                    obj
                )
            )
            for player in players:
                StateOfPlay.add_player(player)

