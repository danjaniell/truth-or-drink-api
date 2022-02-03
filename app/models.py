import json
from enum import IntEnum
from pydantic import BaseModel
from typing import Any
from urllib.request import urlopen


class DeckType(IntEnum):
    OnTheRocks = (1,)
    ExtraDirty = (2,)
    HappyHour = (3,)
    LastCall = (4,)
    WithATwist = 5

    def get_me():
        value: dict[str, int] = {}
        for deck in DeckType:
            value[deck.name] = int(deck)
        return value


class Card(BaseModel):
    card_type: str
    prompts: list[str]
    from_deck: DeckType


class CardResponse(BaseModel):
    count: int
    cards: list

    def __init__(__pydantic_self__, **data: Any) -> None:
        data["count"] = len(data["cards"])
        super().__init__(**data)


class CardCollection(dict[str, Card]):
    def __init__(self, source: str):
        """
        Load file and store contents
        """
        json_file = json.loads(str(urlopen(source).read(), encoding="utf-8"))

        for key, value in json_file.items():
            id: int = 0
            for item in value:
                self[self.generate_key(DeckType[key], id)] = item
                id = id + 1

    def generate_key(self, deck_type: DeckType, id: int):
        return f"{deck_type.name}_{id}"


class StartRequest(BaseModel):
    players: list[str]
