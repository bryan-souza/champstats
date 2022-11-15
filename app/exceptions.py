from typing import Optional


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id: Optional[str] = None):
        _message = f'{self.entity_name} not found'
        if entity_id:
            _message = f'{self.entity_name} not found, id: {entity_id}'
        super().__init__(_message)


class AlreadyExistsError(Exception):
    entity_name: str

    def __init__(self):
        super().__init__(f'{self.entity_name} already exists')


class GameNotFoundError(NotFoundError):
    entity_name = 'Game'


class UserNotFoundError(NotFoundError):
    entity_name = 'User'


class ChampionshipNotFoundError(NotFoundError):
    entity_name = 'Championship'


class MatchNotFoundError(NotFoundError):
    entity_name = 'Match'


class IndexNotFoundError(NotFoundError):
    entity_name = 'Index'


class UserAlreadyExistsError(AlreadyExistsError):
    entity_name = 'User'


class AccountDisabledError(Exception):
    def __init__(self, user_id):
        super().__init__(f'Account for user {user_id} is disabled')


class EmailNotVerifiedError(Exception):
    def __init__(self, email):
        super().__init__(f'Email {email} was not verified')
