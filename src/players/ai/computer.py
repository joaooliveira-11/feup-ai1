import os
import time
from typing import List
import csv
import psutil
from src.models.entity import Entity
from src.utils.gamestate import GameState
from src.models.player import Player
from src.utils.position import Position
from src.entities.tile import Tile

import pygame
import sys

class Computer(Player):

    KEY_PRESS_EVENTS = {
        'enter': pygame.USEREVENT + 1
    }

    def __init__(self, position, sprite, screen, tiles, entities, winPositions, goal_states, level, algorithmName, hint):
        super().__init__(position, sprite, screen)

        self.playerPosition = (position.x, position.y)
        self.tilesPositions = []
        self.whitePositions = []
        self.blackPositions = []
        self.winningPositions = []
        self.alternateWinningPositions = {}
        self.path = []
        self.pathIndex = -1
        
        self.goal_state = [(goal_state[0], goal_state[1]) for goal_state in goal_states]

        for tile in tiles:
            self.tilesPositions.append((tile.position.x, tile.position.y))
        
        for entity in entities:
            if entity.color == "WHITE":
                self.whitePositions.append((entity.position.x, entity.position.y))
            else:
                self.blackPositions.append((entity.position.x, entity.position.y))
                self.tilesPositions.remove((entity.position.x, entity.position.y))
        
        for knight, position in winPositions:
            self.winningPositions.append((knight, (position.x, position.y)))

        for knight, position in winPositions:
            if (position.x, position.y) in self.alternateWinningPositions:
                self.alternateWinningPositions[(position.x, position.y)].append(knight)
            else:
                self.alternateWinningPositions[(position.x, position.y)] = [knight]

        self.initial_state = GameState(self.playerPosition, self.whitePositions)
        start = time.time()
        self.path = self.get_solution(self.initial_state)
        end = time.time()
        process = psutil.Process(os.getpid())
        
        if (hint == False):    
            print("\n")
            print("=====================================")
            print("Level: ", level.currentLevel)
            print("Time taken: ", end - start, " seconds")
            print("Process memory: ", process.memory_info().rss / (1024*1024), "MB")

            self.currentLevel = level.currentLevel
        self.time = end - start
        self.memory = process.memory_info().rss / (1024*1024)
        self.algorithm = algorithmName

        
    def get_solution(self, initial_state):
        """
            Builds the solution path of the problem
            Needs to be implemented by subclass
        """
        return NotImplementedError
    
    def checkWin(self, state):

        """
            Check if the current state is a winning state
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
    
    def new_move_state(self, state, direction):

        """
            Check if the move is valid, if so, return the new state
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
                    return GameState(newPlayerPosition, newWhitePositions)
                else:
                    return None

        for blackknightpos in self.blackPositions:
            if newPlayerPosition == blackknightpos:
                return None

        if newPlayerPosition in [pos for pos in self.tilesPositions] and newPlayerPosition != state.playerPosition:
            return GameState(newPlayerPosition, newWhitePositions)
        else:
            return None

    def generate_possible_moves(self, gamestate):

        """
            Generate all possible moves from the current state
        """

        possible_moves = []
        for move in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_gameState = self.new_move_state(gamestate, move)
            if new_gameState is not None:
                possible_moves.append(new_gameState)
        return possible_moves
    
    def move(self, tiles : List[Tile], entities : List[Entity]):

        """
            Updates the game state to the next state in the path and move its entities to the new positions
        """

        new_game_state = self.path[self.pathIndex]
        
        self.position = Position(new_game_state.playerPosition[0], new_game_state.playerPosition[1])

        white_index = 0
        for entity in entities:
            if entity.color == "WHITE":
                entity.position = Position(new_game_state.whitePositions[white_index][0], new_game_state.whitePositions[white_index][1])
                white_index += 1
        
        return True
    
    def update(self, dashboard):

        """
            Update the game state
        """
        
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == pygame.K_RETURN:
                    self.pathIndex += 1
                    dashboard.key_states['enter'] = True
                    pygame.time.set_timer(self.KEY_PRESS_EVENTS['enter'], 100, True)
                    return "Move"
                
                if event.key == pygame.K_ESCAPE:
                    self.leave = True
            elif event.type in self.KEY_PRESS_EVENTS.values():
                for key, event_id in self.KEY_PRESS_EVENTS.items():
                    if event.type == event_id:
                        dashboard.key_states[key] = False
                        break
        
        return None
    
    def heuristic(self, state):
        """
            Heuristic function to estimate the cost of reaching the goal state
            1. If a white knight is stuck in a corner, add a penalty, acts as a pruning mechanism
            2. Get the distance of each white knight to the closest goal position
            3. Add a penalty if the white knight is not in the goal position
        """
        # First try heuristic
        # piece_mobility = 0
        # manhattan_distance_to_winning_positions = 0
        # manhattan_distance_to_move = 0
                
        # checkedPositions = []
        # checkedWhiteKnights = []
        # distances = []
        # whiteAdjacentPositions = []
        
        # for white_knight in state.whitePositions:
        #     moves = [(0,1), (0,-1), (1,0), (-1,0)]
        #     for move in moves:
        #         new_position = (white_knight[0] + move[0], white_knight[1] + move[1])
        #         if new_position in self.tilesPositions and new_position not in state.whitePositions and new_position not in self.blackPositions and new_position != state.playerPosition:
        #             whiteAdjacentPositions.append(new_position)
                    
        # for position in whiteAdjacentPositions:
        #     distances.append(abs(position[0] - state.playerPosition[0]) + abs(position[1] - state.playerPosition[1]))
        
        # manhattan_distance_to_move += min(distances)
        
        # distances = []
        # for black_knight, checking_position in self.winningPositions:
        #     if checking_position not in checkedPositions:
        #         for white_knight in state.whitePositions:
        #             if white_knight not in checkedWhiteKnights and white_knight != checking_position:
        #                 checkedWhiteKnights.append(white_knight)
        #                 distances.append(abs(white_knight[0] - checking_position[0]) + abs(white_knight[1] - checking_position[1]))
        #             else:
        #                 checkedPositions.append(checking_position)
        #                 distances.append(-1000)
        #         manhattan_distance_to_winning_positions += min(distances)
        
        # weighted_sum = 0 * piece_mobility + 0.2 * manhattan_distance_to_winning_positions + 0.8 * manhattan_distance_to_move
        # normalized = weighted_sum / 3
        
        # return -normalized
        
        # ========================================================================================================
        # Second try heuristic
        # total_distance = 0
        # penalty = 0
        
        # usedBlackKnights = []
        # for black_knight, checking_position in self.winningPositions:
        #     nearest_white_knight = None
        #     nearest_distance = 1000
        #     usedWhiteKnights = []
            
        #     if black_knight not in usedBlackKnights:
        #         for white_knight in state.whitePositions:
        #             if white_knight not in usedWhiteKnights:
        #                 distance = abs(white_knight[0] - checking_position[0]) + abs(white_knight[1] - checking_position[1])
        #                 if distance < nearest_distance:
        #                     nearest_distance = distance
        #                     nearest_white_knight = white_knight
                        
        #         usedWhiteKnights.append(nearest_white_knight)
        #         total_distance += nearest_distance
                
        #         if nearest_white_knight != checking_position:
        #             penalty += 4 # Big influence in the time taken to solve the problem, 5 gives optimal solution in 34 seconds, 100 gives good but not optimal solution in 7 seconds
                
        #     usedBlackKnights.append(black_knight)
            
        # return total_distance + penalty
    # ========================================================================================================
        # Third try heuristic
        # usedBlackKnights = []
        # for black_knight, checking_position in self.winningPositions:
        #     nearest_white_knight = None
        #     nearest_distance = 1000
        #     usedWhiteKnights = []

        #     if black_knight in usedBlackKnights:
        #         continue
            
        #     for white_knight in state.whitePositions:
        #             distance = abs(white_knight[0] - checking_position[0]) + abs(white_knight[1] - checking_position[1])
        #             if distance < nearest_distance:
        #                 nearest_distance = distance
        #                 nearest_white_knight = white_knight

        #     # usedWhiteKnights.append(nearest_white_knight)
        #     total_distance += nearest_distance

        #     if nearest_white_knight != checking_position:
        #         penalty += 4

        #     usedBlackKnights.append(black_knight)



        # for checking_position in self.alternateWinningPositions.keys():
        #     nearest_white_knight = None

        # print("Heuristic: ", total_distance + penalty)
        # return total_distance + 
        
        # ============================================================================================================

        total_distance = 0
        penalty = 0
        
        # If white knight stuck in a corner, add a penalty
        corners = [((0,-1), (-1,0)), ((0,-1), (1,0)), ((0,1), (-1,0)), ((0,1), (1,0))]
        for white_knight in state.whitePositions:
            if white_knight in self.goal_state:
                continue
            for corner in corners:
                new_position_1 = (white_knight[0] + corner[0][0], white_knight[1] + corner[0][1])
                new_position_2 = (white_knight[0] + corner[1][0], white_knight[1] + corner[1][1])
                if new_position_1 not in self.tilesPositions and new_position_2 not in self.tilesPositions:
                    penalty += 10000
                    return penalty
        
        # get the distance of each closest white knight to each goal position
        white_knights = list(state.whitePositions)
        for position in self.goal_state:
            white_knight, distance = min([(white_knight, abs(white_knight[0] - position[0]) + abs(white_knight[1] - position[1])) for white_knight in white_knights], key=lambda x: x[1])
            total_distance += distance
            
            # If distance is 0, this means that the white knight is already in the goal position
            if distance != 0:
                penalty += 4
            
            white_knights.remove(white_knight)
            
            
        return total_distance + penalty

    def resultsToCSV(self, algorithm, level, time, memory, moves):
        """
            Write the results to a CSV file
        """
        with open('results.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([algorithm, level, time, memory, moves])