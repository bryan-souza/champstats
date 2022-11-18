from beanie import Document
from typing import List, Optional

from pydantic import Field


class Game(Document):
    id: Optional[int] = Field()
    nome: str
    descricao: str
    qnt_camp: int
    campeonatos: List[int] = []

    class Settings:
        name = 'games'
