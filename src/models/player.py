from src.models.entity import Entity

class Player(Entity):
    def __init__(self, position, sprite, screen):
        super().__init__(position, sprite, screen)
        self.leave = False


    def update(self, tiles, entities):
        
        """
            Subclass must implement this method to update the player's position
        """

        return False