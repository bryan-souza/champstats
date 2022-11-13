from app.controllers import ChampionshipController
from app.models import Match
from app.exceptions import MatchNotFoundError


class MatchController:
    def __init__(self):
        # HACK: Synchronization with championships collection
        self._championship_controller: ChampionshipController = ChampionshipController()

    async def get_all(self):
        return await Match.find_all().to_list()

    async def get_by_id(self, match_id):
        _match = await Match.get(match_id)
        if not _match:
            raise MatchNotFoundError(match_id)
        return _match

    async def insert(self, champ_id: str, match: Match):
        _match = await Match.insert_one(match)
        _championship = await self._championship_controller.get_by_id(champ_id)
        _championship.partidas.append(_match.id)
        await self._championship_controller.update(champ_id, _championship)
        return _match

    async def update(self, match_id, match: Match):
        _match = await Match.get(match_id)
        if not _match:
            raise MatchNotFoundError(match_id)

        await _match.set(match.dict(exclude_unset=True))
        return _match

    async def delete(self, champ_id, match_id):
        _match = await Match.get(match_id)
        if not _match:
            raise MatchNotFoundError(match_id)

        _championship = await self._championship_controller.get_by_id(champ_id)
        _championship.partidas.remove(match_id)
        await self._championship_controller.update(champ_id, _championship)

        return await _match.delete()
