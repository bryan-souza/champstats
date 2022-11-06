from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, EmailStr
from beanie import Document, Indexed


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(UserUpdate):
    email: Indexed(EmailStr, unique=True)
    disabled: bool = False


class User(Document, UserOut):
    password: str
    email_confirmed_at: Optional[datetime] = None

    @property
    def created(self):
        return self.id.generation_time

    @classmethod
    async def by_email(cls, email: str):
        return await cls.find_one(cls.email == email)


class AccessToken(BaseModel):
    access_token: str
    access_token_expires: timedelta = timedelta(minutes=15)


class RefreshToken(AccessToken):
    refresh_token: str
    refresh_token_expires: timedelta = timedelta(days=30)


class Game(Document):
    nome: str
    descricao: str
    qnt_camp: int

    class Settings:
        name = 'games'
