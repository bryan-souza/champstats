from app.models import Game
from app.exceptions import GameNotFoundError
from app.utils.indexes import IndexService


class GameController:
    def __init__(self):
        self._index_service: IndexService = IndexService()

    async def get_all(self):
        return await Game.find_all().to_list()

    async def get_by_id(self, game_id):
        _game = await Game.get(game_id)
        if not _game:
            raise GameNotFoundError(game_id)
        return _game

    async def insert(self, game: Game):
        game.id = await self._index_service.get_new_game_index()
        return await Game.insert_one(game)

    async def update(self, game_id, game: Game):
        _game = await Game.get(game_id)
        if not _game:
            raise GameNotFoundError(game_id)

        await _game.set(game.dict(exclude={'id': True}, exclude_unset=True))

        return _game

    async def delete(self, game_id):
        _game = await Game.get(game_id)
        if not _game:
            raise GameNotFoundError(game_id)
        return await _game.delete()
