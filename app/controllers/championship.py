from beanie import PydanticObjectId

from app.controllers import GameController
from app.models import Championship
from app.exceptions import ChampionshipNotFoundError


class ChampionshipController:
    def __init__(self):
        # HACK: Synchronization with games collection
        self._game_controller: GameController = GameController()

    async def get_all(self, game_id):
        _game = await self._game_controller.get_by_id(game_id)
        if _game is None:
            return []

        _championships = _game.campeonatos
        _championships = await Championship.find(Championship.id in _championships).to_list()
        return _championships

    async def get_by_id(self, champ_id):
        _champ = await Championship.get(champ_id)
        if not _champ:
            raise ChampionshipNotFoundError(champ_id)
        return _champ

    async def insert(self, game_id, champ: Championship):
        _champ = await Championship.insert_one(champ)
        _game = await self._game_controller.get_by_id(game_id)
        _game.campeonatos.append(_champ.id)
        await self._game_controller.update(game_id, _game)
        return _champ

    async def update(self, champ_id, champ: Championship):
        _champ = await Championship.get(champ_id)
        if not _champ:
            raise ChampionshipNotFoundError(champ_id)

        await _champ.set(champ.dict(exclude_unset=True))
        return _champ

    async def delete(self, game_id, champ_id):
        _champ = await Championship.get(champ_id)
        if not _champ:
            raise ChampionshipNotFoundError(champ_id)

        try:
            _game = await self._game_controller.get_by_id(game_id)
            _game.partidas.remove(PydanticObjectId(champ_id))
            await self._game_controller.update(game_id, _game)
        # This prevents removal of non-synchronized data
        except ValueError:
            pass

        return await _champ.delete()
