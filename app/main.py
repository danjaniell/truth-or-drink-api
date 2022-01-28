import json
from . import models
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
source = "https://gist.githubusercontent.com/danjaniell/f88d4789a388f645c4fea29f89e7f47e/raw/9fe6a255587f3577781f0547c861352773fc6cbe/truth-or-drink_cards.json"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    """
    Disables caching in vercel
    """
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/decks")
def get_decks():
    decks = models.DeckType.get_me()
    return JSONResponse(content=decks)


card_collection = models.CardCollection(source)


@app.get("/all-cards/from-deck/{from_deck}")
def get_all_cards_from_deck(from_deck: models.DeckType):
    cards = [item for item in card_collection.values()
             if item["from_deck"] == from_deck]
    response = json.loads(models.CardResponse(cards=cards).json())
    return JSONResponse(content=response)


@app.get("/all-cards")
def get_all_cards():
    cards = [item for item in card_collection.values()]
    response = json.loads(models.CardResponse(cards=cards).json())
    return JSONResponse(content=response)


@app.get("/draw", response_model=models.Card)
def draw(id: str):
    card = card_collection[id]
    return card
