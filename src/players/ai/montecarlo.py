import sys
import time
from typing import List
import pygame
from src.models.entity import Entity
from src.utils.gamestate import GameState
from src.models.player import Player
from src.utils.position import Position
from src.entities.tile import Tile
from src.utils.node import TreeNode

import random
import math
import numpy as np
from collections import defaultdict

def print_level(tiles, white_positions, black_positions, player_position):
    """
    Prints level information in a comprehensible way. Used for debugging
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

class monteCarlo2(Player):
    def __init__(self, position, sprite, screen, tiles, entities, winPositions, exploration_weight=2):
        super().__init__(position, sprite, screen)

        self.playerPosition = (position.x, position.y)
        self.tilesPositions = []
        self.whitePositions = []
        self.blackPositions = []
        self.winningPositions = []
        self.pathIndex = 0

        for tile in tiles:
            self.tilesPositions.append((tile.position.x, tile.position.y))

        for entity in entities:
            if entity.color == "WHITE":
                self.whitePositions.append((entity.position.x, entity.position.y))
            else:
                self.blackPositions.append((entity.position.x, entity.position.y))

        for knight, position in winPositions:
            self.winningPositions.append((knight, (position.x, position.y)))

#--------------------------------------------------------------------------------
        state = GameState(self.playerPosition, self.whitePositions)
        root_node = TreeNode(state)
        children = self.find_children(state)
        children_list = []
        for child in children:
            child_node = TreeNode(child)
            root_node.add_child(child_node)
            children_list.append(child_node)

        self.root = root_node

        self.path = []
        self.path.append(state)

        start = time.time()
        self.path = self.Run()
        end = time.time()

        print("Time taken:", end - start)
    
    def Selection(self):
        """
        Responsible for the selection phase of the algorithm
        """
        SelectedChild = self.root
        HasChild = False

		# Check if child nodes exist.
        if(len(SelectedChild.children) > 0):
            HasChild = True
        else:
            HasChild = False
            
        while(HasChild):
            SelectedChild = self.SelectChild(SelectedChild)
            if(len(SelectedChild.children) == 0):
                HasChild  = False

        return SelectedChild
    
    def SelectChild(self, Node):
        """
        Selects child of argument node
        """
        if(len(Node.children) == 0):
            return Node
        
        for Child in Node.children:
            if(Child.visits > 0.0):
                continue
            else:
                return Child

        MaxWeight = 0.0
        for Child in Node.children:
            Weight = Child.sputc
            if(Weight > MaxWeight):
                MaxWeight = Weight
                SelectedChild = Child
        return SelectedChild
    
    def Expansion(self, Leaf):
        """
        Responsible for the expansion phase of the algorithm
        """
        if (self.isTerminal(Leaf.state)):
            print("Is Terminal.")
            return False
        elif(Leaf.visits == 0):
            return Leaf
        else:
            # Expand.
            if(len(Leaf.children) == 0):
                Children = self.EvalChildren(Leaf) #nodes 
                for NewChild in Children:
                    if(np.all(NewChild.state == Leaf.state)):
                        continue
                    Leaf.add_child(NewChild)
            assert (len(Leaf.children) > 0), "Error"
            Child = self.SelectChildNode(Leaf)

        return Child

    def isTerminal(self, state):
        """
        Checks if given state is a terminal state
        """
        if self.checkWin(state):
            return True
        if (self.find_children(state) == []):
            return True
        return False
    
    def isTerminalNode(self, node):
        """
        Checks if given node is a terminal node
        """
        if self.checkWin(node.state):
            return True
        if (self.find_children(node.state) == []):
            return True
        return False
    
    def EvalChildren(self, Node):
        """
        Obtains all possible child states of a given node
        """
        NextStates = self.find_children(Node.state)
        Children = []
        for State in NextStates:
            ChildNode = TreeNode(State)
            Children.append(ChildNode)

        return Children
    
        # All possible successors of this board state
    def find_children(self, state):
        """
        All possible successors of this board state
        """
        possible_moves = []
        for move in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_gameState = self.new_move_state(state, move)
            if new_gameState is not None:
                
                possible_moves.append(new_gameState)
        return possible_moves
    
    # Check if the player can move to the new position
    def new_move_state(self, state, direction):
        """
        Check if the player can move to the new position
        """
        newPlayerPosition = (state.playerPosition[0] + direction[0], state.playerPosition[1] + direction[1])
        newWhitePositions = state.whitePositions
        
        for i, whiteknightpos in enumerate(state.whitePositions):

            if newPlayerPosition == whiteknightpos:
                nextKnightPosition = (whiteknightpos[0] + direction[0], whiteknightpos[1] + direction[1])
                if nextKnightPosition not in state.whitePositions and nextKnightPosition in self.tilesPositions and nextKnightPosition not in self.blackPositions:
                    newWhitePositions = [
                        pos if i != j else nextKnightPosition for j, pos in enumerate(state.whitePositions)
                    ]
                    game = GameState(newPlayerPosition, newWhitePositions)
                    
                    return GameState(newPlayerPosition, newWhitePositions)
                else:
                    return None

        for blackknightpos in self.blackPositions:
            if newPlayerPosition == blackknightpos:
                return None

        if newPlayerPosition in [pos for pos in self.tilesPositions] and newPlayerPosition != state.playerPosition:
            game = GameState(newPlayerPosition, newWhitePositions)
            return GameState(newPlayerPosition, newWhitePositions)
        else:
            return None

    def getNextState(self, state): 
        """
        Randomly selects child state
        """
        children = self.find_children(state)

        Len = len(children)
        assert Len > 0, "Incorrect length"
        i = np.random.randint(0, Len)
        return children[i]        
    	
    def SelectChildNode(self, Node):
        # Randomly selects a child node.
        """
        Randomly select child node
        """
        Len = len(Node.children)
        assert Len > 0, "Incorrect length"
        i = np.random.randint(0, Len)
        return Node.children[i]

    def Simulation(self, Node):
        """
        Responsible for the simulation phase of the algorithm
        """
        CurrentState = Node.state

        Level = self.GetLevel(Node)
        # Perform simulation.
        for _ in range(1000):
            CurrentState = self.getNextState(CurrentState)
            
            if (self.isTerminal(CurrentState)):
                break
            Level += 1.0

        Result = self.heuristic(CurrentState)
        return Result
    
    def GetLevel(self, Node):
        """
        Obtains depth of given node
        """
        Level = 0.0
        while(Node.parent):
            Level += 1.0
            Node = Node.parent
        return Level

    def heuristic(self, state):
        """
        Previous heuristic function. Meanwhile changed for the rest of the game.
        """      
        total_distance = 0
        penalty = 0
        
        usedBlackKnights = []
        for black_knight, checking_position in self.winningPositions:
            nearest_white_knight = None
            nearest_distance = 1000
            usedWhiteKnights = []
            
            if black_knight not in usedBlackKnights:
                for white_knight in state.whitePositions:
                    if white_knight not in usedWhiteKnights:
                        distance = abs(white_knight[0] - checking_position[0]) + abs(white_knight[1] - checking_position[1])
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_white_knight = white_knight
                        
                usedWhiteKnights.append(nearest_white_knight)
                total_distance += nearest_distance
                
                if nearest_white_knight != checking_position:
                    penalty += 5 # Big influence in the time taken to solve the problem, 5 gives optimal solution in 34 seconds, 100 gives good but not optimal solution in 7 seconds
                
            usedBlackKnights.append(black_knight)
            
        return total_distance + penalty
    
    def Backpropagation(self, Node, Result):
        """
        Responsible for the backpropagation phase of the algorithm
        """
		# Update Node's weight.
        CurrentNode = Node
        CurrentNode.wins += Result
        CurrentNode.ressq += Result**2
        CurrentNode.visits += 1
        self.EvalUTC(CurrentNode)

        while(self.HasParent(CurrentNode)):
            # Update parent node's weight.
            CurrentNode = CurrentNode.parent
            CurrentNode.wins += Result
            CurrentNode.ressq += Result**2
            CurrentNode.visits += 1
            self.EvalUTC(CurrentNode)

    def HasParent(self, Node):
        """
        Returns True if given node has a parent
        """
        if(Node.parent == None):
            return False
        else:
            return True
        
    def EvalUTC(self, Node):
        """
        Evaluates node according to the Upper Confidence Bound
        """
        #c = np.sqrt(2)
        c = 0.5
        w = Node.wins
        n = Node.visits
        sumsq = Node.ressq
        if(Node.parent == None):
            t = Node.visits
        else:
            t = Node.parent.visits

        UTC = w/n + c * np.sqrt(np.log(t)/n)
        D = 10000.
        Modification = np.sqrt((sumsq - n * (w/n)**2 + D)/n)

        Node.sputc = UTC + Modification
        return Node.sputc
    
    def Run(self, MaxIter = 500):
        """
        Runs algorithm with MaxIter iterations
        """
        best_node = None
        best_win_rate = -1
        best_path = None

        for i in range(MaxIter):
            path = []  # List to store the states visited during this iteration
            X = self.Selection()
            path.append(X.state)  # Add the selected state to the path

            Y = self.Expansion(X)
            
            if(Y):
                path.append(Y.state)  # Add the expanded state to the path
                
                Result = self.Simulation(Y)
                self.Backpropagation(Y, Result)
            else:
                Result = self.heuristic(X.state)
                self.Backpropagation(X, Result)
 
            win_rate = X.wins / X.visits if X.visits != 0 else 0
            if win_rate > best_win_rate:
                best_win_rate = win_rate
                best_node = X
                best_path = path  # Store the path of this iteration as the new best path

        return best_path if best_node else None

    def checkWin(self, state):
        """
        Check winning condition
        """
        white_to_black = {}
        
        
        for black_knight, checking_position in self.winningPositions:
            for white_knight in state.whitePositions:
                if white_knight == checking_position:
                    if white_knight in white_to_black:
                        white_to_black[white_knight].append(black_knight)
                    else:
                        white_to_black[white_knight] = [black_knight]
        
        every_white_is_checking_a_black = True
        for white_knight in state.whitePositions:
            if white_knight not in white_to_black:
                every_white_is_checking_a_black = False
                break
            
        for white_knight, black_knights in white_to_black.items():
            for white_knight2, black_knights2 in white_to_black.items():
                if white_knight != white_knight2 and len(black_knights) == len(black_knights2) == 1:
                    if black_knights[0] == black_knights2[0]:
                        every_white_is_checking_a_black = False
                        break
            
        checkedBlackKnights = set()
        for white_knight, black_knights in white_to_black.items():
            checkedBlackKnights.update(black_knights)
        

        if every_white_is_checking_a_black and checkedBlackKnights == set([knight for knight, _ in self.winningPositions]):
            return True
        
        return False
    
    def update(self, dashboard):
        """
        Update game cycle
        """
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == pygame.K_RETURN:
                    self.pathIndex += 1
                    return "Move"
        
        return None
    
    def move(self, tiles : List[Tile], entities : List[Entity]):
        """
        moves entity
        """
        new_game_state = self.path[self.pathIndex]
        
        self.position = Position(new_game_state.playerPosition[0], new_game_state.playerPosition[1])

        white_index = 0
        for entity in entities:
            if entity.color == "WHITE":
                entity.position = Position(new_game_state.whitePositions[white_index][0], new_game_state.whitePositions[white_index][1])
                white_index += 1
        
        return True
