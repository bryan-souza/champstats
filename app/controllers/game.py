from app.models import Game
from app.exceptions import GameNotFoundError


class GameController:
    def __init__(self):
        ...

    async def get_all(self):
        return await Game.find_all().to_list()

    async def get_by_id(self, game_id):
        _game = await Game.get(game_id)
        if not _game:
            raise GameNotFoundError(game_id)
        return _game

    async def insert(self, game: Game):
        return await Game.insert_one(game)

    async def update(self, game_id, game: Game):
        _game = await Game.get(game_id)
        if not _game:
            raise GameNotFoundError(game_id)
        return await _game.update(game)

    async def delete(self, game_id):
        _game = await Game.get(game_id)
        if not _game:
            raise GameNotFoundError(game_id)
        return await Game.delete()
