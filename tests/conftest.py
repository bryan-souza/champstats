import pytest
from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT

from app.server import app
from app.models import Game
from app.controllers import GameController


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_authentication(monkeypatch):
    def mock_jwt_required(*args, **kwargs):
        return None

    def mock_jwt_refresh_token_required(*args, **kwargs):
        return None

    monkeypatch.setattr(AuthJWT, 'jwt_required', mock_jwt_required)
    monkeypatch.setattr(AuthJWT, 'jwt_refresh_token_required', mock_jwt_refresh_token_required)
    yield
    monkeypatch.delattr(AuthJWT, 'jwt_refresh_token_required')
    monkeypatch.delattr(AuthJWT, 'jwt_required')


@pytest.fixture
def mock_game_controller(monkeypatch):
    async def mock_get_all(*args, **kwargs):
        return [Game(nome='Test Game', descricao='Game for Testing Purposes', qnt_camp=0)]

    async def mock_get_by_id(*args, **kwargs):
        return Game(nome='Test Game', descricao='Game for Testing Purposes', qnt_camp=0)

    async def mock_insert(*args, **kwargs):
        return Game(nome='Test Game', descricao='Game for Testing Purposes', qnt_camp=0)

    async def mock_update(*args, **kwargs):
        return Game(nome='Test Game', descricao='Game for Testing Purposes', qnt_camp=0)

    async def mock_delete(*args, **kwargs):
        return None

    monkeypatch.setattr(GameController, 'get_all', mock_get_all)
    monkeypatch.setattr(GameController, 'get_by_id', mock_get_by_id)
    monkeypatch.setattr(GameController, 'insert', mock_insert)
    monkeypatch.setattr(GameController, 'update', mock_update)
    monkeypatch.setattr(GameController, 'delete', mock_delete)
    yield
    monkeypatch.delattr(GameController, 'delete')
    monkeypatch.delattr(GameController, 'update')
    monkeypatch.delattr(GameController, 'insert')
    monkeypatch.delattr(GameController, 'get_by_id')
    monkeypatch.delattr(GameController, 'get_all')
