import os
import bcrypt

from app.utils import Singleton
from app.config import CONFIG


class PasswordService(metaclass=Singleton):
    def __init__(self):
        self._salt = CONFIG.salt

    def hash_password(self, password: str) -> bytes:
        b_password = bytes(password, encoding='UTF-8')
        return bcrypt.hashpw(b_password, self._salt)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        b_password = bytes(password, encoding='UTF-8')
        h_password = bytes(hashed_password, encoding='UTF-8')
        return bcrypt.checkpw(b_password, h_password)
