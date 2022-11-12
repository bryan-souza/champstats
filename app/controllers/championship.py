from app.models import Championship
from app.exceptions import ChampionshipNotFoundError


class ChampionshipController:
    def __init__(self):
        ...

    async def get_all(self):
        return await Championship.find_all().to_list()

    async def get_by_id(self, champ_id):
        _champ = await Championship.get(champ_id)
        if not _champ:
            raise ChampionshipNotFoundError(champ_id)
        return _champ

    async def insert(self, champ: Championship):
        return await Championship.insert_one(champ)

    async def update(self, champ_id, champ: Championship):
        _champ = await Championship.get(champ_id)
        if not _champ:
            raise ChampionshipNotFoundError(champ_id)

        await _champ.set(champ.dict(exclude_unset=True))
        return _champ

    async def delete(self, champ_id):
        _champ = await Championship.get(champ_id)
        if not _champ:
            raise ChampionshipNotFoundError(champ_id)
        return await _champ.delete()
