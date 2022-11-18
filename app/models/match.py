from beanie import Document
from typing import List, Optional
from datetime import time

from pydantic import Field

from app.utils import encoders


class Match(Document):
    id: Optional[int] = Field()
    equipes: List[str]
    duracao: time
    vencedor: str
    placar: str

    class Settings:
        name = 'matches'
        bson_encoders = {
            time: encoders.time_encoder
        }
