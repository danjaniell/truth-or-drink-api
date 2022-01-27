import json
from . import models
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()


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
    decks = json.dumps(decks)
    return JSONResponse(content=decks)


card_collection = models.CardCollection()


@app.get("/allCards")
def get_all_cards_from_deck(from_deck: models.DeckType):
    if (from_deck == 0):
        return JSONResponse(content=card_collection)
    cards = [item for item in card_collection.values()
             if item["from_deck"] == from_deck]
    return JSONResponse(content=cards)


@app.get("/draw", response_model=models.Card)
def draw(id: str):
    card = card_collection[id]
    return card
