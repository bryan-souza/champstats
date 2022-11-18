import pytest
from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT
from pymongo.results import DeleteResult

from app.server import app
from app.controllers import ChampionshipController, GameController
from app.models import Championship, Game
from app.exceptions import GameNotFoundError, ChampionshipNotFoundError


def test_get_all_championships(client, monkeypatch):
    test_data = [
        Championship(nome="CBLoL 2021", equipes=["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                     premiacao=25000, local="Praça da Sé, São Paulo, Brasil", lotacao=200000,
                     situacao="Concluído"),
        Championship(nome="CBLoL 2022", equipes=["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                     premiacao=25000, local="Praça da Sé, São Paulo, Brasil", lotacao=200000,
                     situacao="Concluído"),
        Championship(nome="CBLoL 2023", equipes=["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                     premiacao=25000, local="Praça da Sé, São Paulo, Brasil", lotacao=200000,
                     situacao="Em andamento"),
    ]

    async def mock_get_all(*args, **kwargs):
        return test_data

    monkeypatch.setattr(ChampionshipController, "get_all", mock_get_all)

    response = client.get('/jogos/0/campeonatos/')
    assert response.status_code == 200
    assert response.json() == [
        {'_id': None, 'nome': 'CBLoL 2021', 'equipes': ["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
         'vencedor': None, 'premiacao': 25000.0, 'mvp': None, 'local': 'Praça da Sé, São Paulo, Brasil',
         'lotacao': 200000, 'datas': None, 'situacao': 'Concluído', 'partidas': []},
        {'_id': None, 'nome': 'CBLoL 2022', 'equipes': ["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
         'vencedor': None, 'premiacao': 25000.0, 'mvp': None, 'local': 'Praça da Sé, São Paulo, Brasil',
         'lotacao': 200000, 'datas': None, 'situacao': 'Concluído', 'partidas': []},
        {'_id': None, 'nome': 'CBLoL 2023', 'equipes': ["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
         'vencedor': None, 'premiacao': 25000.0, 'mvp': None, 'local': 'Praça da Sé, São Paulo, Brasil',
         'lotacao': 200000, 'datas': None, 'situacao': 'Em andamento', 'partidas': []},
    ]

    # monkeypatch cleanup
    monkeypatch.delattr(ChampionshipController, 'get_all')


def test_insert_championship(client, monkeypatch, mock_authentication):
    test_data = Championship(nome="CBLoL 2021", equipes=["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                             premiacao=25000, local="Praça da Sé, São Paulo, Brasil", lotacao=200000,
                             situacao="Concluído")

    async def mock_insert_championship(*args, **kwargs):
        return test_data

    monkeypatch.setattr(ChampionshipController, 'insert', mock_insert_championship)

    response = client.post('/jogos/0/campeonatos/',
                           json={'nome': 'CBLoL 2021', 'equipes': ["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                                 'premiacao': 25000, 'local': 'Praça da Sé, São Paulo, Brasil', 'lotacao': 200000,
                                 'situacao': 'Concluído'})

    assert response.status_code == 201
    assert response.json() == {'_id': None, 'nome': 'CBLoL 2021',
                               'equipes': ["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                               'vencedor': None, 'premiacao': 25000.0, 'mvp': None,
                               'local': 'Praça da Sé, São Paulo, Brasil',
                               'lotacao': 200000, 'datas': None, 'situacao': 'Concluído', 'partidas': []}

    monkeypatch.delattr(ChampionshipController, 'insert')


def test_insert_championship_422(client, monkeypatch, mock_authentication):
    test_data = Championship(nome="CBLoL 2021", equipes=["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                             premiacao=25000, local="Praça da Sé, São Paulo, Brasil", lotacao=200000,
                             situacao="Concluído")

    async def mock_insert(*args, **kwargs):
        return test_data

    monkeypatch.setattr(ChampionshipController, 'insert', mock_insert)

    response = client.post('/jogos/0/campeonatos/',
                           json={'nome': 'CBLoL 2021', 'equipes': ["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                                 'premiacao': 25000, 'local': 'Praça da Sé, São Paulo, Brasil', 'lotacao': 200000})
    assert response.status_code == 422

    monkeypatch.delattr(ChampionshipController, 'insert')


def test_get_championship_by_id(client, monkeypatch):
    test_data = Championship(nome="CBLoL 2021", equipes=["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                             premiacao=25000, local="Praça da Sé, São Paulo, Brasil", lotacao=200000,
                             situacao="Concluído")

    async def mock_get_by_id(*args, **kwargs):
        return test_data

    monkeypatch.setattr(ChampionshipController, 'get_by_id', mock_get_by_id)

    response = client.get('/jogos/0/campeonatos/0')
    assert response.status_code == 200
    assert response.json() == {'_id': None, 'nome': 'CBLoL 2021',
                               'equipes': ["LOUD", "Renga", "RED Kalunga", "Pain Gaming"],
                               'vencedor': None, 'premiacao': 25000.0, 'mvp': None,
                               'local': 'Praça da Sé, São Paulo, Brasil',
                               'lotacao': 200000, 'datas': None, 'situacao': 'Concluído', 'partidas': []}

    # monkeypatch cleanup
    monkeypatch.delattr(ChampionshipController, 'get_by_id')


def test_get_championship_by_id_404(client, monkeypatch):
    async def mock_get_by_id_404(champ_id, *args, **kwargs, ):
        raise ChampionshipNotFoundError(champ_id)

    monkeypatch.setattr(ChampionshipController, 'get_by_id', mock_get_by_id_404)

    response = client.get('/jogos/0/campeonatos/0')
    assert response.status_code == 404

    # monkeypatch cleanup
    monkeypatch.delattr(ChampionshipController, 'get_by_id')


def test_update_championship(client, monkeypatch, mock_authentication):
    test_data = Championship(nome="CBLoL 2021", equipes=["Netshoes Miners", "Renga", "RED Kalunga", "Pain Gaming"],
                             premiacao=25000, local="Praça da Sé, São Paulo, Brasil", lotacao=200000,
                             situacao="Concluído")

    async def mock_update(*args, **kwargs):
        return test_data

    monkeypatch.setattr(ChampionshipController, 'update', mock_update)

    response = client.put('/jogos/0/campeonatos/0',
                          json={'nome': 'CBLoL 2021',
                                'equipes': ["Netshoes Miners", "Renga", "RED Kalunga", "Pain Gaming"],
                                'premiacao': 25000, 'local': 'Praça da Sé, São Paulo, Brasil', 'lotacao': 200000,
                                'situacao': 'Concluído'})
    assert response.status_code == 200
    assert response.json() == {'_id': None, 'nome': 'CBLoL 2021',
                               'equipes': ["Netshoes Miners", "Renga", "RED Kalunga", "Pain Gaming"],
                               'vencedor': None, 'premiacao': 25000.0, 'mvp': None,
                               'local': 'Praça da Sé, São Paulo, Brasil',
                               'lotacao': 200000, 'datas': None, 'situacao': 'Concluído', 'partidas': []}

    monkeypatch.delattr(ChampionshipController, 'update')


def test_update_championship_422(client, monkeypatch, mock_authentication):
    test_data = Championship(nome="CBLoL 2021", equipes=["Netshoes Miners", "Renga", "RED Kalunga", "Pain Gaming"],
                             premiacao=25000, local="Praça da Sé, São Paulo, Brasil", lotacao=200000,
                             situacao="Concluído")

    async def mock_update(*args, **kwargs):
        return test_data

    monkeypatch.setattr(ChampionshipController, 'update', mock_update)

    response = client.put('/jogos/0/campeonatos/0',
                          json={'nome': 'CBLoL 2021',
                                'equipes': ["Netshoes Miners", "Renga", "RED Kalunga", "Pain Gaming"],
                                'premiacao': 25000, 'local': 'Praça da Sé, São Paulo, Brasil', 'lotacao': 200000})
    assert response.status_code == 422

    monkeypatch.delattr(ChampionshipController, 'update')


def test_update_championship_404(client, monkeypatch, mock_authentication):
    async def mock_update(champ_id, *args, **kwargs):
        raise ChampionshipNotFoundError(champ_id)

    monkeypatch.setattr(ChampionshipController, 'update', mock_update)

    response = client.put('/jogos/0/campeonatos/0',
                          json={'nome': 'CBLoL 2021',
                                'equipes': ["Netshoes Miners", "Renga", "RED Kalunga", "Pain Gaming"],
                                'premiacao': 25000, 'local': 'Praça da Sé, São Paulo, Brasil', 'lotacao': 200000,
                                'situacao': 'Concluído'})
    assert response.status_code == 404

    monkeypatch.delattr(ChampionshipController, 'update')


def test_delete_championship(client, monkeypatch, mock_authentication):
    async def mock_delete(champ_id, *args, **kwargs):
        return DeleteResult({}, acknowledged=True)

    monkeypatch.setattr(ChampionshipController, 'delete', mock_delete)

    response = client.delete('/jogos/0/campeonatos/0')
    assert response.status_code == 204

    monkeypatch.delattr(ChampionshipController, 'delete')


def test_delete_championship_404(client, monkeypatch, mock_authentication):
    async def mock_delete(champ_id, *args, **kwargs):
        raise ChampionshipNotFoundError(champ_id)

    monkeypatch.setattr(ChampionshipController, 'delete', mock_delete)

    response = client.delete('/jogos/0/campeonatos/0')
    assert response.status_code == 404

    monkeypatch.delattr(ChampionshipController, 'delete')
