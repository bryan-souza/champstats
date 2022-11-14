from datetime import time

import pytest

from app.controllers import MatchController
from app.exceptions import MatchNotFoundError
from app.models import Match


@pytest.fixture
def fake_match():
    obj = Match(equipes=["LOUD", "Pain Gaming"], duracao=time(minute=30), vencedor="LOUD", placar="20 X 15")
    json = {'_id': None, 'equipes': ["LOUD", "Pain Gaming"], 'duracao': '00:30:00', 'vencedor': 'LOUD',
            'placar': '20 X 15'}

    return obj, json


@pytest.fixture
def fake_match_list():
    obj_list = [
        Match(equipes=["LOUD", "Pain Gaming"], duracao=time(minute=30), vencedor="LOUD", placar="20 X 15"),
        Match(equipes=["Rensga", "Kabum"], duracao=time(minute=33), vencedor="Kabum", placar="10 X 15"),
        Match(equipes=["LOUD", "Miners"], duracao=time(minute=31), vencedor="Miners", placar="10 X 12")
    ]

    json_list = [
        {'_id': None, 'equipes': ["LOUD", "Pain Gaming"], 'duracao': '00:30:00', 'vencedor': 'LOUD',
         'placar': '20 X 15'},
        {'_id': None, 'equipes': ["Rensga", "Kabum"], 'duracao': '00:33:00', 'vencedor': 'Kabum',
         'placar': '10 X 15'},
        {'_id': None, 'equipes': ["LOUD", "Miners"], 'duracao': '00:31:00', 'vencedor': 'Miners',
         'placar': '10 X 12'}
    ]

    return obj_list, json_list


def test_get_all_matches(client, monkeypatch, fake_match_list):
    test_data, test_json = fake_match_list

    async def mock_get_all(*args, **kwargs):
        return test_data

    monkeypatch.setattr(MatchController, 'get_all', mock_get_all)

    response = client.get('/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/')
    assert response.status_code == 200
    assert response.json() == test_json

    monkeypatch.delattr(MatchController, 'get_all')


def test_insert_match(client, monkeypatch, fake_match, mock_authentication):
    test_data, test_json = fake_match

    async def mock_insert(*args, **kwargs):
        return test_data

    monkeypatch.setattr(MatchController, 'insert', mock_insert)

    response = client.post('/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/',
                           json={'equipes': ["LOUD", "Pain Gaming"], 'duracao': '00:30:00', 'vencedor': 'LOUD',
                                 'placar': '20 X 15'})
    assert response.status_code == 201
    assert response.json() == test_json

    monkeypatch.delattr(MatchController, 'insert')


def test_insert_match_422(client, monkeypatch, fake_match, mock_authentication):
    test_data, test_json = fake_match

    async def mock_insert(*args, **kwargs):
        return test_data

    monkeypatch.setattr(MatchController, 'insert', mock_insert)

    response = client.post('/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/',
                           json={'equipes': ["LOUD", "Pain Gaming"], 'duracao': '00:30:00', 'vencedor': 'LOUD'})
    assert response.status_code == 422

    monkeypatch.delattr(MatchController, 'insert')


def test_get_match_by_id(client, monkeypatch, fake_match):
    test_data, test_json = fake_match

    async def mock_get_by_id(*args, **kwargs):
        return test_data

    monkeypatch.setattr(MatchController, 'get_by_id', mock_get_by_id)

    response = client.get(
        '/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/636ff4f095781437f0693cf4')

    assert response.status_code == 200
    assert response.json() == test_json

    monkeypatch.delattr(MatchController, 'get_by_id')


def test_get_match_by_id_404(client, monkeypatch):
    async def mock_get_by_id(match_id, *args, **kwargs):
        raise MatchNotFoundError(match_id)

    monkeypatch.setattr(MatchController, 'get_by_id', mock_get_by_id)

    response = client.get(
        '/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/636ff4f095781437f0693cf4')

    assert response.status_code == 404

    monkeypatch.delattr(MatchController, 'get_by_id')


def test_update_match(client, monkeypatch, mock_authentication):
    test_data = Match(equipes=["LOUD", "Pain Gaming"], duracao=time(minute=32), vencedor="LOUD", placar="20 X 15")
    test_json = {'_id': None, 'equipes': ["LOUD", "Pain Gaming"], 'duracao': '00:32:00', 'vencedor': 'LOUD',
                 'placar': '20 X 15'}

    async def mock_update(*args, **kwargs):
        return test_data

    monkeypatch.setattr(MatchController, 'update', mock_update)

    response = client.put(
        '/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/636ff4f095781437f0693cf4',
        json={'equipes': ["LOUD", "Pain Gaming"], 'duracao': '00:32:00', 'vencedor': 'LOUD', 'placar': '20 X 15'}
    )

    assert response.status_code == 200
    assert response.json() == test_json

    monkeypatch.delattr(MatchController, 'update')


def test_update_match_404(client, monkeypatch, mock_authentication):
    async def mock_update(match_id, *args, **kwargs):
        raise MatchNotFoundError(match_id)

    monkeypatch.setattr(MatchController, 'update', mock_update)

    response = client.put(
        '/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/636ff4f095781437f0693cf4',
        json={'equipes': ["LOUD", "Pain Gaming"], 'duracao': '00:32:00', 'vencedor': 'LOUD', 'placar': '20 X 15'}
    )

    assert response.status_code == 404

    monkeypatch.delattr(MatchController, 'update')


def test_update_match_422(client, monkeypatch, mock_authentication):
    test_data = Match(equipes=["LOUD", "Pain Gaming"], duracao=time(minute=32), vencedor="LOUD", placar="20 X 15")

    async def mock_update(*args, **kwargs):
        return test_data

    monkeypatch.setattr(MatchController, 'update', mock_update)

    response = client.put(
        '/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/636ff4f095781437f0693cf4',
        json={'equipes': ["LOUD", "Pain Gaming"], 'duracao': '00:32:00', 'vencedor': 'LOUD'}
    )

    assert response.status_code == 422

    monkeypatch.delattr(MatchController, 'update')


def test_delete_match(client, monkeypatch, mock_authentication):
    async def mock_delete(*args, **kwargs):
        return None

    monkeypatch.setattr(MatchController, 'delete', mock_delete)

    response = client.delete(
        '/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/636ff4f095781437f0693cf4'
    )

    assert response.status_code == 204

    monkeypatch.delattr(MatchController, 'delete')


def test_delete_match_404(client, monkeypatch, mock_authentication):
    async def mock_delete(match_id, *args, **kwargs):
        raise MatchNotFoundError(match_id)

    monkeypatch.setattr(MatchController, 'delete', mock_delete)

    response = client.delete(
        '/jogos/6366d398e11697c77d2281aa/campeonatos/636ff4f095781437f0693cf4/partidas/636ff4f095781437f0693cf4'
    )

    assert response.status_code == 404

    monkeypatch.delattr(MatchController, 'delete')
