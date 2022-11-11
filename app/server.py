import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models import Game, User
from app.routers import game, auth
from app.config import CONFIG

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return CONFIG


@app.exception_handler(AuthJWTException)
def jwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


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
