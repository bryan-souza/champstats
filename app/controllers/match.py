from beanie import PydanticObjectId

from app.controllers import ChampionshipController
from app.models import Match
from app.exceptions import MatchNotFoundError, ChampionshipNotFoundError
from app.utils.indexes import IndexService


class MatchController:
    def __init__(self):
        self._championship_controller: ChampionshipController = ChampionshipController()
        self._index_service: IndexService = IndexService()

    async def __get_matches_in_championship(self, game_id, champ_id):
        _champ = await self._championship_controller.get_by_id(game_id, champ_id)
        if _champ is None:
            raise ChampionshipNotFoundError(champ_id)

        return _champ.partidas

    async def get_all(self, game_id, champ_id):
        _matches = await self.__get_matches_in_championship(game_id, champ_id)
        _matches = await Match.find_all(Match.id in _matches).to_list()
        return _matches

    async def get_by_id(self, game_id, champ_id, match_id):
        _matches = await self.__get_matches_in_championship(game_id, champ_id)
        if match_id not in _matches:
            raise MatchNotFoundError(match_id)

        _match = await Match.get(match_id)
        if _match is None:
            raise MatchNotFoundError(match_id)

        return _match

    async def insert(self, game_id, champ_id, match: Match):
        match.id = await self._index_service.get_new_match_index()
        _match = await Match.insert_one(match)

        _championship = await self._championship_controller.get_by_id(game_id, champ_id)
        _championship.partidas.append(_match.id)
        await self._championship_controller.update(game_id, champ_id, _championship)
        return _match

    async def update(self, game_id, champ_id, match_id, match: Match):
        _matches = await self.__get_matches_in_championship(game_id, champ_id)
        if match_id not in _matches:
            raise MatchNotFoundError(match_id)

        _match = await Match.get(match_id)
        if _match is None:
            raise MatchNotFoundError(match_id)

        await _match.set(match.dict(exclude={'id': True}, exclude_unset=True))
        return _match

    async def delete(self, game_id, champ_id, match_id):
        _matches = await self.__get_matches_in_championship(game_id, champ_id)
        if match_id not in _matches:
            raise MatchNotFoundError(match_id)

        _match = await Match.get(match_id)
        if _match is None:
            raise MatchNotFoundError(match_id)

        try:
            _championship = await self._championship_controller.get_by_id(game_id, champ_id)
            _championship.partidas.remove(PydanticObjectId(match_id))
            await self._championship_controller.update(game_id, champ_id, _championship)
        # This prevents removal of non-synchronized data
        except ValueError:
            pass

        return await _match.delete()
