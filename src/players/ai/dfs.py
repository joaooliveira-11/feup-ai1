from collections import deque
from src.utils.node import TreeNode
from src.players.ai.computer import Computer

class Dfs(Computer):

    def __init__(self, position, sprite, screen, tiles, entities, winPositions, level, algorithmName):
        super().__init__(position, sprite, screen, tiles, entities, winPositions, [], level, algorithmName, False)
        
        print("Number of moves: ", len(self.path))
        print("=====================================")

        self.resultsToCSV(self.algorithm, self.currentLevel, self.time, self.memory, len(self.path))

    def depth_first_search(self, initial_state, goal_state_func, operators_func):

        """
            Depth-first search algorithm to find the goal state
        """

        root = TreeNode(initial_state)
        reached = set([initial_state]) 
        stack = deque([root]) 

        while stack:
            node = stack.pop()
            if goal_state_func(node.state):
                return node
            
            for state in operators_func(node.state):
                new_node = TreeNode(state)
                new_node.parent = node
                new_node.depth = node.depth + 1

                if new_node.state not in reached:
                    reached.add(new_node.state)
                    stack.append(new_node)
    
        return None
    
    def get_solution(self, initial_state):
        
        """
            Get the solution path from the initial state to the goal state
        """
        
        solution = self.depth_first_search(initial_state, self.checkWin, self.generate_possible_moves)

        path = []
        currentNode =  solution
        while currentNode.parent is not None:
            path.append(currentNode.state)
            currentNode = currentNode.parent
    
        path = path[::-1]
        return path