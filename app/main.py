from . import startup
from . import models
from . import services
from fastapi.responses import JSONResponse
import json
import random

app = startup.app
redisDb = startup.redisDb
card_collection = models.CardCollection(startup.source)


@app.get("/decks")
def get_decks():
    """
    Returns all deck types
    """
    decks = models.DeckType.get_me()
    return JSONResponse(content=decks)


@app.get("/all-cards/from-deck/{from_deck}")
def get_all_cards_from_deck(from_deck: models.DeckType):
    """
    Return all cards in a given deck
    """
    cards = [
        item for item in card_collection.values() if item["from_deck"] == from_deck
    ]
    response = json.loads(models.CardResponse(cards=cards).json())
    return JSONResponse(content=response)


@app.get("/all-cards")
def get_all_cards():
    """
    Return all cards
    """
    cards = [item for item in card_collection.values()]
    response = json.loads(models.CardResponse(cards=cards).json())
    return JSONResponse(content=response)


@app.get("/draw", response_model=models.Card)
def draw():
    """
    Randomly Draw a Card
    """
    card = random.choice(list(card_collection.values()))
    return card


@app.get("/draw/from-deck/{deck_type}", response_model=models.Card)
def draw(deck_type: models.DeckType):
    """
    Randomly Draw a Card from a specified deck
    """
    deck = list(
        filter(lambda x: x["from_deck"] == deck_type, list(card_collection.values()))
    )
    card = random.choice(deck)
    return card


@app.post("/start")
def start(request: models.StartRequest):
    if redisDb.get("Current"):
        return False

    sid = "SESH-" + services.generate_id(4)
    redisDb.set("Current", sid)

    session = {"PL-" + services.generate_id(3): i for i in request.players}
    redisDb.hmset(sid, session)

    return True
