from app.models import Match
from app.exceptions import MatchNotFoundError


class MatchController:
    def __init__(self):
        ...

    async def get_all(self):
        return await Match.find_all().to_list()

    async def get_by_id(self, match_id):
        _match = await Match.get(match_id)
        if not _match:
            raise MatchNotFoundError(match_id)
        return _match

    async def insert(self, match: Match):
        return await Match.insert_one(match)

    async def update(self, match_id, match: Match):
        _match = await Match.get(match_id)
        if not _match:
            raise MatchNotFoundError(match_id)

        await _match.set(match.dict(exclude_unset=True))
        return _match

    async def delete(self, match_id):
        _match = await Match.get(match_id)
        if not _match:
            raise MatchNotFoundError(match_id)
        return await _match.delete()
