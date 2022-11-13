from datetime import datetime, timedelta
from typing import Optional, List

from pydantic import BaseModel, EmailStr
from beanie import Document, Indexed, PydanticObjectId


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

    class Settings:
        name = 'users'


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
    campeonatos: List[PydanticObjectId] = []

    class Settings:
        name = 'games'


class Championship(Document):
    nome: str
    equipes: List[str]
    vencedor: Optional[str] = None
    premiacao: float
    mvp: Optional[str] = None
    local: str
    lotacao: Optional[int] = None
    datas: Optional[List[datetime]] = None
    situacao: str
    partidas: List[PydanticObjectId] = []

    class Settings:
        name = 'championships'
