from typing import Optional


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id: Optional[str] = None):
        _message = f'{self.entity_name} not found'
        if entity_id:
            _message = f'{self.entity_name} not found, id: {entity_id}'
        super().__init__(_message)


class GameNotFoundError(NotFoundError):
    entity_name = 'Game'


class UserNotFoundError(NotFoundError):
    entity_name = 'User'
