from collections import deque
from src.utils.node import TreeNode
from src.players.ai.computer import Computer

class IDDfs(Computer):

    def __init__(self, position, sprite, screen, tiles, entities, winPositions, level, algorithmName, hint):
        super().__init__(position, sprite, screen, tiles, entities, winPositions, [], level, algorithmName, hint)
        
        if (hint == False):
            print("Number of moves: ", len(self.path))
            print("=====================================")
        
            self.resultsToCSV(self.algorithm, self.currentLevel, self.time, self.memory, len(self.path))
    
    def depth_first_search(self, initial_state, goal_state_func, operators_func, depth):

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
            
            if node.depth < depth:
                for state in operators_func(node.state):
                    new_node = TreeNode(state)
                    new_node.parent = node
                    new_node.depth = node.depth + 1

                    if new_node.state not in reached:
                        reached.add(new_node.state)
                        stack.append(new_node)
    
        return None
    
    def iterative_deepening_search(self, initial_state, goal_state_func, operators_func):

        """
            Iterative deepening search algorithm to find the goal state
        """

        depth = 0
        while True:
            result = self.depth_first_search(initial_state, goal_state_func, operators_func, depth)
            if result is not None:
                return result
            depth += 1
    
    def get_solution(self, initial_state):

        """
            Get the solution path from the initial state to the goal state
        """
        
        solution = self.iterative_deepening_search(initial_state, self.checkWin, self.generate_possible_moves)
        
        path = []
        currentNode =  solution
        while currentNode.parent is not None:
            path.append(currentNode.state)
            currentNode = currentNode.parent
    
        path = path[::-1]
        return path