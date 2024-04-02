class GameState:
    def __init__(self, playerPosition, whitePositions):
        self.playerPosition = playerPosition
        self.whitePositions = whitePositions

    
    def __eq__(self, __value: object) -> bool:
        for i, pos in enumerate(self.whitePositions):
            if pos != __value.whitePositions[i]:
                return False
        return self.playerPosition == __value.playerPosition
    
    def __hash__(self) -> int:
        return hash((self.playerPosition, tuple(self.whitePositions)))
    
    def __str__(self) -> str:
        return f"Player: {self.playerPosition}, Whites: {self.whitePositions}"