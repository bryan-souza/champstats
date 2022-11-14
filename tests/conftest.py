import pytest
from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT

from app.server import app


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
