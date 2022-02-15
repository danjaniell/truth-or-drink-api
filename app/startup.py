import os
from redis import Redis
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

app = FastAPI()

load_dotenv("../.env")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redisDb = Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    db=0,
    socket_timeout=None,
)

source = os.getenv("SOURCE")


@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    """
    Disables caching in vercel
    """
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response
