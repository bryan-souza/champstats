import os

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models import Game, User
from app.routers import game, auth
from app.config import CONFIG

app = FastAPI()


@app.on_event('startup')
async def on_server_start():
    client = AsyncIOMotorClient(CONFIG.mongo_uri)
    await init_beanie(
        database=client.champstats,
        document_models=[Game, User]
    )

    # TODO: Include routers
    app.include_router(auth.router)
    app.include_router(game.router)
