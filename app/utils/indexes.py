from app.controllers import IndexController
from app.models import Index
from app.utils import Singleton


class IndexService(metaclass=Singleton):
    _index_controller: IndexController = IndexController()

    async def create_default_index(self):
        return await self._index_controller.insert(Index())

    async def get_new_game_index(self):
        _index = await self._index_controller.get()
        if _index is None:
            _index = await self.create_default_index()

        _index.game_index = _index.game_index + 1
        await self._index_controller.update(_index.id, _index)
        return _index.game_index

    async def get_new_champ_index(self):
        _index = await self._index_controller.get()
        if _index is None:
            _index = await self.create_default_index()

        _index.championship_index = _index.championship_index + 1
        await self._index_controller.update(_index.id, _index)
        return _index.championship_index

    async def get_new_match_index(self):
        _index = await self._index_controller.get()
        if _index is None:
            _index = await self.create_default_index()

        _index.match_index = _index.match_index + 1
        await self._index_controller.update(_index.id, _index)
        return _index.match_index
