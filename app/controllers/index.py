from app.models import Index
from app.exceptions import IndexNotFoundError


class IndexController:
    def __init__(self):
        pass

    async def get_all(self):
        return await Index.find_all().to_list()

    async def get_by_id(self, index_id):
        _index = await Index.get(index_id)
        if _index is None:
            raise IndexNotFoundError(index_id)

        return _index

    async def insert(self, index: Index):
        return await Index.insert(index)

    def update(self, index_id, index: Index):
        _index = await Index.get(index_id)
        if _index is None:
            raise IndexNotFoundError(index_id)

        await _index.set(index.dict(exclude_unset=True))
        return _index

    def delete(self, index_id):
        _index = await Index.get(index_id)
        if _index is None:
            raise IndexNotFoundError(index_id)

        return await _index.delete()
