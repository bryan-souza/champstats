from beanie import Document, PydanticObjectId
from typing import List


class Game(Document):
    nome: str
    descricao: str
    qnt_camp: int
    campeonatos: List[PydanticObjectId] = []

    class Settings:
        name = 'games'
