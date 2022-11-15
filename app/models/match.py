from beanie import Document
from typing import List
from datetime import time
from app.utils import encoders


class Match(Document):
    equipes: List[str]
    duracao: time
    vencedor: str
    placar: str

    class Settings:
        name = 'matches'
        bson_encoders = {
            time: encoders.time_encoder
        }
