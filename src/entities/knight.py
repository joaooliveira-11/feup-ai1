from src.models.entity import Entity

class Knight(Entity):
    def __init__(self, position, sprite, screen, color):
        super().__init__(position, sprite, screen)
        self.color = color

    def move(self, position):

        """
            Move the knight to a new position
        """
        
        self.position = position
    