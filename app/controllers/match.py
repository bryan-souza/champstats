from beanie import PydanticObjectId

from app.controllers import ChampionshipController
from app.models import Match
from app.exceptions import MatchNotFoundError, ChampionshipNotFoundError


class MatchController:
    def __init__(self):
        self._championship_controller: ChampionshipController = ChampionshipController()

    async def __get_matches_in_championship(self, champ_id):
        _champ = await self._championship_controller.get_by_id(champ_id)
        if _champ is None:
            raise ChampionshipNotFoundError(champ_id)

        return _champ.partidas

    async def get_all(self, champ_id):
        _matches = await self.__get_matches_in_championship(champ_id)
        _matches = await Match.find_all(Match.id in _matches).to_list()
        return _matches

    async def get_by_id(self, champ_id, match_id):
        _matches = await self.__get_matches_in_championship(champ_id)
        if match_id not in _matches:
            raise MatchNotFoundError(match_id)

        _match = await Match.get(match_id)
        if _match is None:
            raise MatchNotFoundError(match_id)

        return _match

    async def insert(self, champ_id: str, match: Match):
        _match = await Match.insert_one(match)
        _championship = await self._championship_controller.get_by_id(champ_id)
        _championship.partidas.append(_match.id)
        await self._championship_controller.update(champ_id, _championship)
        return _match

    async def update(self, champ_id, match_id, match: Match):
        _matches = await self.__get_matches_in_championship(champ_id)
        if match_id not in _matches:
            raise MatchNotFoundError(match_id)

        _match = await Match.get(match_id)
        if _match is None:
            raise MatchNotFoundError(match_id)

        await _match.set(match.dict(exclude_unset=True))
        return _match

    async def delete(self, champ_id, match_id):
        _matches = await self.__get_matches_in_championship(champ_id)
        if match_id not in _matches:
            raise MatchNotFoundError(match_id)

        _match = await Match.get(match_id)
        if _match is None:
            raise MatchNotFoundError(match_id)

        try:
            _championship = await self._championship_controller.get_by_id(champ_id)
            _championship.partidas.remove(PydanticObjectId(match_id))
            await self._championship_controller.update(champ_id, _championship)
        # This prevents removal of non-synchronized data
        except ValueError:
            pass

        return await _match.delete()
