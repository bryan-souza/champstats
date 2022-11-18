from app.models import Index
from app.exceptions import IndexNotFoundError


class IndexController:
    def __init__(self):
        pass

    async def get(self):
        # Since there should be only one object, no need to search
        # for its id, neither to get all indexes
        return await Index.find_all().first_or_none()

    async def insert(self, index: Index):
        return await Index.insert(index)

    async def update(self, index_id, index: Index):
        _index = await Index.get(index_id)
        if _index is None:
            raise IndexNotFoundError(index_id)

        await _index.set(index.dict(exclude_unset=True))
        return _index

    async def delete(self, index_id):
        _index = await Index.get(index_id)
        if _index is None:
            raise IndexNotFoundError(index_id)

        return await _index.delete()
