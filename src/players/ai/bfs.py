from collections import deque
from src.utils.node import TreeNode
from src.players.ai.computer import Computer

class Bfs(Computer):

    def __init__(self, position, sprite, screen, tiles, entities, winPositions, level, algorithmName):
        super().__init__(position, sprite, screen, tiles, entities, winPositions, [], level, algorithmName, False)
        print("Number of moves: ", len(self.path))
        print("=====================================")
        
        self.resultsToCSV(self.algorithm, self.currentLevel, self.time, self.memory, len(self.path))
    
    def breadth_first_search(self, initial_state, goal_state_func, operators_func):

        """
            Breadth-first search algorithm to find the goal state
        """

        root = TreeNode(initial_state)   # create the root node in the search tree
        queue = deque([root])   # initialize the queue to store the nodes
        reached = set([initial_state])  # keep track of visited states

        if goal_state_func(initial_state): 
            return root
    
        while queue:
            node = queue.popleft()   # get first element in the queue

            for state in operators_func(node.state):   # go through next states
                # create tree node with the new state
                new_node = TreeNode(state)
                
                # link child node to its parent in the tree
                new_node.parent = node

                if goal_state_func(new_node.state):
                    return new_node

                if new_node.state not in reached:
                    queue.append(new_node)
                    reached.add(new_node.state)
    
    def get_solution(self, initial_state):

        """
            Get the solution path from the initial state to the goal state
        """
        
        path = []

        solution = self.breadth_first_search(initial_state, self.checkWin, self.generate_possible_moves)
        currentNode =  solution
        while currentNode.parent is not None:
            path.append(currentNode.state)
            currentNode = currentNode.parent
    
        path = path[::-1]
        return path
    
    
                