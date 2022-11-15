from beanie import PydanticObjectId

from app.controllers import GameController
from app.models import Championship
from app.exceptions import ChampionshipNotFoundError, GameNotFoundError


class ChampionshipController:
    def __init__(self):
        self._game_controller: GameController = GameController()

    async def __get_championships_of_game(self, game_id):
        _game = await self._game_controller.get_by_id(game_id)
        if _game is None:
            raise GameNotFoundError(game_id)
        return _game.campeonatos

    async def get_all(self, game_id):
        _championships = await self.__get_championships_of_game(game_id)
        _championships = await Championship.find(Championship.id in _championships).to_list()
        return _championships

    async def get_by_id(self, game_id, champ_id):
        _championships = await self.__get_championships_of_game(game_id)

        if champ_id not in _championships:
            return ChampionshipNotFoundError(champ_id)

        _champ = await Championship.get(champ_id)
        if _champ is None:
            return ChampionshipNotFoundError(champ_id)

        return _champ

    async def insert(self, game_id, champ: Championship):
        _champ = await Championship.insert_one(champ)
        _game = await self._game_controller.get_by_id(game_id)
        _game.campeonatos.append(_champ.id)
        _game.qnt_camp = len(_game.campeonatos)
        await self._game_controller.update(game_id, _game)
        return _champ

    async def update(self, game_id, champ_id, champ: Championship):
        _championships = await self.__get_championships_of_game(game_id)
        if champ_id not in _championships:
            raise ChampionshipNotFoundError(champ_id)

        _champ = await Championship.get(champ_id)
        if _champ is None:
            return ChampionshipNotFoundError(champ_id)

        await _champ.set(champ.dict(exclude_unset=True))
        return _champ

    async def delete(self, game_id, champ_id):
        _championships = await self.__get_championships_of_game(game_id)
        if champ_id not in _championships:
            raise ChampionshipNotFoundError(champ_id)

        _champ = await Championship.get(champ_id)
        if _champ is None:
            raise ChampionshipNotFoundError(champ_id)

        try:
            _game = await self._game_controller.get_by_id(game_id)
            _game.partidas.remove(PydanticObjectId(champ_id))
            _game.qnt_camp = len(_game.campeonatos)
            await self._game_controller.update(game_id, _game)
        # This prevents removal of non-synchronized data
        except ValueError:
            pass

        return await _champ.delete()
