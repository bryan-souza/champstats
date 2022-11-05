import os

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models import Game
from app.routers import game

app = FastAPI()


@app.on_event('startup')
async def on_server_start():
    try:
        client = AsyncIOMotorClient(os.environ['DB_URL'])
        await init_beanie(
            database=client.get_default_database(),
            document_models=[Game]
        )
    except KeyError:
        # TODO: Log error
        raise

    # TODO: Include routers
    app.include_router(game.router)
