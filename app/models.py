import json
from enum import IntEnum
from pydantic import BaseModel


class DeckType(IntEnum):
    All = 0
    OnTheRocks = 1,
    ExtraDirty = 2,
    HappyHour = 3,
    LastCall = 4,
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


class CardCollection(dict[str, Card]):
    def __init__(self, source="./app/cards.json"):
        """
        Load file and store contents
        """
        json_file = json.loads(open(source, "r").read())

        for key, value in json_file.items():
            id: int = 0
            for item in value:
                self[self.generate_key(DeckType[key], id)] = item
                id = id + 1

    def generate_key(self, deck_type: DeckType, id: int):
        return f"{deck_type.name}_{id}"
