from src.models.entity import Entity

class Tile(Entity):
    def __init__(self, position, sprite, screen):
        super().__init__(position, sprite, screen)
        self.color = "WHITE" if (position.x + position.y) % 2 == 0 else "BLACK"
        