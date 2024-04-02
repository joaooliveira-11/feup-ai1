import sys
from typing import List
from src.utils.gamestate import GameState
from src.players.ai.computer import Computer

def print_level(tiles, white_positions, black_positions, player_position):
    height = max([pos[1] for pos in tiles]) + 1
    width = max([pos[0] for pos in tiles]) + 1

    for y in range(height):
        for x in range(width+1):
            if (x, y) == player_position:
                print("P", end=" ")
            elif (x, y) in white_positions:
                print("W", end=" ")
            elif (x, y) in black_positions:
                print("B", end=" ")
            elif (x, y) in [(tile[0], tile[1]) for tile in tiles]:
                print("□", end=" ")
            else:
                print(" ", end=" ")
        print()

    print()

class IDAStar(Computer):
    def __init__(self, position, sprite, screen, tiles, entities, winPositions, goal_state, level, algorithmName):
        super().__init__(position, sprite, screen, tiles, entities, winPositions, goal_state, level, algorithmName, False)
        self.pathIndex = 0
        print("Number of moves: ", len(self.path)-1)
        print("=====================================")
        
        self.resultsToCSV(self.algorithm, self.currentLevel, self.time, self.memory, len(self.path)-1)

    def get_solution(self, initial_state):
        """
            Get the solution of the game using the IDA* algorithm
        """
        return self.ida_star(initial_state)
    
    def ida_star(self, state: GameState):
        """
            IDA* algorithm
        """

        bound = self.heuristic(state)
        path = [state]
        visited = set([state]) # Added visited set to avoid infinite loops
        while True:
            t = self.search(path, visited, 0, bound)
            if t == -1:
                return path
            if t == sys.maxsize:
                return None
            bound = t

    def search(self, path: List[GameState], visited, g: int, bound: int):
        """
            Search function for the IDA* algorithm
            Responsible for the recursive search of the solution
        """
        state = path[-1]
        f = g + self.heuristic(state)
        if f > bound:
            return f
        if self.checkWin(state):
            return -1
        min = sys.maxsize

        for child in self.generate_possible_moves(state):
            if child not in visited:
                path.append(child)
                visited.add(child) 
                t = self.search(path, visited, g + 1, bound)
                if t == -1:
                    return -1
                if t < min:
                    min = t
                path.pop()
                visited.remove(child)
                
        return min
        
