from beanie import Document


class Game(Document):
    nome: str
    descricao: str
    qnt_camp: int

    class Settings:
        name = 'games'
