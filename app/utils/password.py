import os
import bcrypt
from app.utils import Singleton


class PasswordService(metaclass=Singleton):
    def __init__(self):
        salt = os.environ.get('PWD_SALT')
        if not salt:
            # TODO: Log error
            raise EnvironmentError('`PWD_SALT` is not set')

        self._salt = bytes(salt, encoding='UTF-8')

    def hash_password(self, password: str) -> bytes:
        b_password = bytes(password, encoding='UTF-8')
        return bcrypt.hashpw(b_password, self._salt)

    def verify_password(self, password: str, hashed_password: bytes) -> bool:
        b_password = bytes(password, encoding='UTF-8')
        return bcrypt.checkpw(b_password, hashed_password)
