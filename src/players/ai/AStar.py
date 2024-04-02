import heapq
from typing import List
from src.players.ai.computer import Computer
from src.utils.node import TreeNode

import settings

def print_level(tiles, white_positions, black_positions, player_position):
    """
    Prints information about the level for debug purposes
    """
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

class AStar(Computer):
    def __init__(self, position, sprite, screen, tiles, entities, winPositions, goal_state, level, algorithmName):
        super().__init__(position, sprite, screen, tiles, entities, winPositions, goal_state, level, algorithmName, False)
        self.pathIndex = 0
        print("Number of moves: ", len(self.path)-1)
        print("=====================================")
        
        self.resultsToCSV(self.algorithm, self.currentLevel, self.time, self.memory, len(self.path)-1)
        
    def get_solution(self, initial_state):
        """
        Runs the A* algorithm
        """
        return self.a_star(initial_state)
    
    def a_star(self, initial_state):
        """
        A* algorithm, Greedy, Weighted A*, Uniform Cost function
        """
        start_node = TreeNode(state=initial_state)
        start_node.g = start_node.h = start_node.f = 0

        open_list = []
        heapq.heappush(open_list, (start_node.f, start_node)) # Using heap as the search time is O(log n), instead of O(n) in a list
        closed_set = set()
        visited_set = set()

        while open_list:
            current_node = heapq.heappop(open_list)[1] # Get the node with the lowest f value
                    
            # Add the current state to the visited set
            visited_set.add(current_node.state)
                    
            # Pop current off open list, add to closed list
            closed_set.add(current_node.state)

            # Found the goal state
            if self.checkWin(current_node.state):
                path = []
                current = current_node
                while current is not None:
                    path.append(current.state)
                    current = current.parent
                return path[::-1]
            
            # Generate children
            children = []
            for new_state in self.generate_possible_moves(current_node.state):
                if new_state not in visited_set:
                    new_node = TreeNode(state=new_state, parent=current_node)
                    children.append(new_node)
            
            # Loop through children
            for child in children:
                
                # Child is on the closed list
                if child.state in closed_set:
                    continue
                
                # Create the f, g, and h values
                child.g = (current_node.g + 1) * settings.G # Specifies whether to use g(n) or not
                child.h = self.heuristic(child.state) * settings.H # Specifies whether to use h(n) or not
                child.f = child.g + (child.h * settings.WEIGHT) # Specifies the weight of the heuristic function

                # Child is already in the open list
                for open_node in open_list:
                    if child.state == open_node[1].state and child.g > open_node[1].g:
                        continue

                # Add the child to the open list
                heapq.heappush(open_list, (child.f, child))
