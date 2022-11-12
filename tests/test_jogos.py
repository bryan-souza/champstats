from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT
from pymongo.results import DeleteResult

from app.server import app
from app.controllers import GameController
from app.models import Game
from app.exceptions import GameNotFoundError


def test_get_all_games(monkeypatch):
    with TestClient(app) as client:
        test_data = [
            Game(nome='League of Legends', descricao='LoL é o maior MOBA do mundo', qnt_camp=150),
            Game(nome='CS:GO', descricao='Counter Strike: Global Offensive', qnt_camp=200),
            Game(nome='FIFA 23', descricao='Mesma coisa do FIFA 22, só que mais caro', qnt_camp=50)
        ]

        async def mock_get_all(*args, **kwargs):
            return test_data

        monkeypatch.setattr(GameController, "get_all", mock_get_all)

        response = client.get('/jogos/')
        assert response.status_code == 200
        assert response.json() == [
            {'_id': None, 'nome': 'League of Legends', 'descricao': 'LoL é o maior MOBA do mundo', 'qnt_camp': 150},
            {'_id': None, 'nome': 'CS:GO', 'descricao': 'Counter Strike: Global Offensive', 'qnt_camp': 200},
            {'_id': None, 'nome': 'FIFA 23', 'descricao': 'Mesma coisa do FIFA 22, só que mais caro', 'qnt_camp': 50}
        ]

        # monkeypatch cleanup
        monkeypatch.delattr(GameController, 'get_all')


def test_insert_game(monkeypatch):
    with TestClient(app) as client:
        def mock_jwt_required(*args, **kwargs):
            return None

        async def mock_insert_game(*args, **kwargs):
            return Game(_id='6366d398e11697c77d2281aa', nome='League of Legends',
                        descricao='LoL é o maior MOBA do mundo',
                        qnt_camp=150)

        monkeypatch.setattr(AuthJWT, 'jwt_required', mock_jwt_required)
        monkeypatch.setattr(GameController, 'insert', mock_insert_game)

        response = client.post('/jogos/', json={'nome': 'League of Legends',
                                                'descricao': 'LoL é o maior MOBA do mundo',
                                                'qnt_camp': 150})
        assert response.status_code == 201
        assert response.json() == {'_id': '6366d398e11697c77d2281aa', 'nome': 'League of Legends',
                                   'descricao': 'LoL é o maior MOBA do mundo', 'qnt_camp': 150}

        monkeypatch.delattr(AuthJWT, 'jwt_required')
        monkeypatch.delattr(GameController, 'insert')


def test_insert_game_422(monkeypatch):
    with TestClient(app) as client:
        async def mock_insert_game(*args, **kwargs):
            return Game(_id='6366d398e11697c77d2281aa', nome='League of Legends',
                        descricao='LoL é o maior MOBA do mundo',
                        qnt_camp=150)

        monkeypatch.setattr(GameController, 'insert', mock_insert_game)

        response = client.post('/jogos/', json={'nome': 'League of Legends', 'qnt_camp': 150})
        assert response.status_code == 422

        monkeypatch.delattr(GameController, 'insert')


def test_get_game_by_id(monkeypatch):
    with TestClient(app) as client:
        test_data = Game(_id='6366d398e11697c77d2281aa', nome='League of Legends',
                         descricao='LoL é o maior MOBA do mundo',
                         qnt_camp=150)

        async def mock_get_by_id(*args, **kwargs):
            return test_data

        monkeypatch.setattr(GameController, 'get_by_id', mock_get_by_id)

        response = client.get('/jogos/6366d398e11697c77d2281aa')
        assert response.status_code == 200
        assert response.json() == {'_id': '6366d398e11697c77d2281aa', 'nome': 'League of Legends',
                                   'descricao': 'LoL é o maior MOBA do mundo', 'qnt_camp': 150}

        # monkeypatch cleanup
        monkeypatch.delattr(GameController, 'get_by_id')


def test_get_game_by_id_404(monkeypatch):
    with TestClient(app) as client:
        async def mock_get_by_id_404(game_id, *args, **kwargs, ):
            raise GameNotFoundError(game_id)

        monkeypatch.setattr(GameController, 'get_by_id', mock_get_by_id_404)

        response = client.get('/jogos/6366d398e11697c77d2281aa')
        assert response.status_code == 404

        # monkeypatch cleanup
        monkeypatch.delattr(GameController, 'get_by_id')


def test_update_game(monkeypatch):
    with TestClient(app) as client:
        def mock_jwt_required(*args, **kwargs):
            return None

        async def mock_update(*args, **kwargs):
            return Game(_id='6366d398e11697c77d2281aa', nome='League of Legends',
                        descricao='LoL é o maior MOBA do mundo',
                        qnt_camp=100)

        monkeypatch.setattr(AuthJWT, 'jwt_required', mock_jwt_required)
        monkeypatch.setattr(GameController, 'update', mock_update)

        response = client.put('/jogos/6366d398e11697c77d2281aa', json={'nome': 'League of Legends',
                                                                       'descricao': 'LoL é o maior MOBA do mundo',
                                                                       'qnt_camp': 100})
        assert response.status_code == 200
        assert response.json() == {
            '_id': '6366d398e11697c77d2281aa',
            'nome': 'League of Legends',
            'descricao': 'LoL é o maior MOBA do mundo',
            'qnt_camp': 100
        }

        monkeypatch.delattr(AuthJWT, 'jwt_required')
        monkeypatch.delattr(GameController, 'update')


def test_update_game_422(monkeypatch):
    with TestClient(app) as client:
        async def mock_update(*args, **kwargs):
            return Game(_id='6366d398e11697c77d2281aa', nome='League of Legends',
                        descricao='LoL é o maior MOBA do mundo',
                        qnt_camp=100)

        monkeypatch.setattr(GameController, 'update', mock_update)

        response = client.put('/jogos/6366d398e11697c77d2281aa', json={'nome': 'League of Legends',
                                                                       'qnt_camp': 100})
        assert response.status_code == 422

        monkeypatch.delattr(GameController, 'update')


def test_update_game_404(monkeypatch):
    with TestClient(app) as client:
        def mock_jwt_required(*args, **kwargs):
            return None

        async def mock_update(game_id, *args, **kwargs):
            raise GameNotFoundError(game_id)

        monkeypatch.setattr(AuthJWT, 'jwt_required', mock_jwt_required)
        monkeypatch.setattr(GameController, 'update', mock_update)

        response = client.put('/jogos/6366d398e11697c77d2281aa', json={'nome': 'League of Legends',
                                                                       'descricao': 'LoL é o maior MOBA do mundo',
                                                                       'qnt_camp': 100})
        assert response.status_code == 404

        monkeypatch.delattr(AuthJWT, 'jwt_required')
        monkeypatch.delattr(GameController, 'update')


def test_delete_game(monkeypatch):
    with TestClient(app) as client:
        def mock_jwt_required(*args, **kwargs):
            return None

        async def mock_delete_game(game_id, *args, **kwargs):
            return DeleteResult({}, acknowledged=True)

        monkeypatch.setattr(AuthJWT, 'jwt_required', mock_jwt_required)
        monkeypatch.setattr(GameController, 'delete', mock_delete_game)

        response = client.delete('/jogos/6366d398e11697c77d2281aa')
        assert response.status_code == 204

        monkeypatch.delattr(AuthJWT, 'jwt_required')
        monkeypatch.delattr(GameController, 'delete')


def test_delete_game_404(monkeypatch):
    with TestClient(app) as client:
        def mock_jwt_required(*args, **kwargs):
            return None

        async def mock_delete_game_404(game_id, *args, **kwargs):
            raise GameNotFoundError(game_id)

        monkeypatch.setattr(AuthJWT, 'jwt_required', mock_jwt_required)
        monkeypatch.setattr(GameController, 'delete', mock_delete_game_404)

        response = client.delete('/jogos/6366d398e11697c77d2281aa')
        assert response.status_code == 404

        monkeypatch.delattr(AuthJWT, 'jwt_required')
        monkeypatch.delattr(GameController, 'delete')
