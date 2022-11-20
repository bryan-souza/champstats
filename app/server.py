from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models import Game, User, Championship, Match, Index
from app.routers import game, auth, championship, match
from app.config import CONFIG

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


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
        document_models=[Game, User, Championship, Match, Index]
    )

    app.include_router(auth.router)
    app.include_router(game.router)
    app.include_router(championship.router)
    app.include_router(match.router)
