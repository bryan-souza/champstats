from beanie import Document, PydanticObjectId
from typing import Optional, List
from datetime import datetime

from pydantic import Field

from app.utils import encoders


class Championship(Document):
    id: Optional[int] = Field()
    nome: str
    equipes: List[str]
    vencedor: Optional[str] = None
    premiacao: str
    mvp: Optional[str] = None
    local: str
    lotacao: Optional[str] = None
    datas: Optional[List[datetime]] = []
    situacao: str
    partidas: List[int] = []

    class Settings:
        name = 'championships'
        bson_encoders = {
            datetime: encoders.datetime_encoder
        }
