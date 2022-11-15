from beanie import Document


class Index(Document):
    game_index: int
    championship_index: int
    match_index: int

    class Settings:
        name = 'indexes'
