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
    premiacao: float
    mvp: Optional[str] = None
    local: str
    lotacao: Optional[int] = None
    datas: Optional[List[datetime]] = None
    situacao: str
    partidas: List[PydanticObjectId] = []

    class Settings:
        name = 'championships'
        bson_encoders = {
            datetime: encoders.datetime_encoder
        }
