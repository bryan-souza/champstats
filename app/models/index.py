from beanie import Document


class Index(Document):
    game_index: int = -1
    championship_index: int = -1
    match_index: int = -1

    class Settings:
        name = 'indexes'
