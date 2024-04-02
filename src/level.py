import pygame
import json 
import sys

from src.players.ai.AStar import AStar
from src.players.ai.IDAStar import IDAStar
from src.players.ai.bfs import Bfs
from src.models.player import Player
from src.entities.tile import Tile
from src.utils.position import Position
from src.entities.knight import Knight
from src.players.human import Human
from src.players.ai.dfs import Dfs
from src.players.ai.IDdfs import IDDfs
from src.players.ai.montecarlo import monteCarlo2

from src.utils.dashboard import AStarDashboard, DfsDashboard, IDDfsDashboard, HumanDashboard, BfsDashboard, IDAStarDashboard, MonteCarloDashboard

import settings

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.leave = False
        self.height = 0
        self.width = 0

        self.tiles = []
        self.entities = []
        self.chosenPlayer = None
        self.player : Player = None

        self.dashboard = None
        self.moveLog = []
        self.winningPositions = []

        self.hint = None
        self.sprite_hint = None

        self.gamewin = False
        self.currentLevel = 0

    def loadLevel(self, level, chosenPlayer):

        """
            Load the level from the JSON file
        """

        self.currentLevel = level
        self.chosenPlayer = chosenPlayer
        with open(f'./levels/level-{level}.json') as f:
            data = json.load(f)

            data = data['level']['board']

            self.height = data['height']
            self.width = data['width']
            self.goal_state = data['goal_state']

            # Set the scale factor to fit the board on the screen
            settings.SCALE_FACTOR = min(settings.WINDOW_SIZE[0] / ((self.width + 1.5)* 32), settings.WINDOW_SIZE[1] / ((self.height + 1.5) * 32))
            self.sprite_hint = pygame.transform.scale(pygame.image.load('./sprites/tile-gold.png'), (32 * settings.SCALE_FACTOR, 32 * settings.SCALE_FACTOR))
            self.hint = None
            
            self.loadEntities(data)

    def loadNextLevel(self, level, chosenPlayer):

        """
            Load the next level
        """

        self.loadLevel(level + 1, chosenPlayer)
    
    def loadEntities(self, data):

        """
            Load the entities from the JSON file
        """

        self.tiles = []
        self.entities = []
        self.winningPositions = []
        self.moveLog = []
        
        # Save entities starting positions
        entitiesStartingPos = []

        for tile in data['tiles']:
            position = Position(tile[0], tile[1])

            spritePath = './sprites/tile-white.png' if (position.x + position.y) % 2 == 0 else './sprites/tile-black.png'
            self.tiles.append(Tile(position, spritePath, self.screen))
        
        for white_knight in data['white']:
            position = Position(white_knight[0], white_knight[1])
            entitiesStartingPos.append(position)
            self.entities.append(Knight(position, './sprites/knight-white.png', self.screen, "WHITE"))

        for black_knight in data['black']:
            position = Position(black_knight[0], black_knight[1])
            entitiesStartingPos.append(position)
            self.entities.append(Knight(position, './sprites/knight-black.png', self.screen, "BLACK"))

        position = Position(data['player'][0], data['player'][1])


        # Calculate winning positions
        for knight in self.entities:
            if knight.color == "BLACK":
                L_Moves = [Position(-2, -1), Position(-2, 1), Position(-1, -2), Position(-1, 2), Position(1, -2), Position(1, 2), Position(2, -1), Position(2, 1)]
                for move in L_Moves:
                    if knight.position + move in [tile.position for tile in self.tiles]:
                        self.winningPositions.append((knight, knight.position + move))

        match self.chosenPlayer:
            case "Human":
                self.player = Human(position, './sprites/pawn.png', self.screen)
                self.dashboard = HumanDashboard(self.screen)
            case "Bfs":
                self.player = Bfs(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self, "Bfs")
                self.dashboard = BfsDashboard(self.screen)    
            case "Dfs":
                self.player = Dfs(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self, "Dfs")
                self.dashboard = DfsDashboard(self.screen)
            case "IDDfs":
                self.player = IDDfs(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self, "IDDfs", False)
                self.dashboard = IDDfsDashboard(self.screen)
            case "A*":
                settings.WEIGHT = 1
                settings.G = 1
                settings.H = 1
                self.player = AStar(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self.goal_state, self, "A*")
                self.dashboard = AStarDashboard(self.screen)
            case "Monte Carlo":
                self.player = monteCarlo2(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self.goal_state)
                self.dashboard = MonteCarloDashboard(self.screen)
            case "Uniform":
                settings.WEIGHT = 0
                settings.G = 1
                settings.H = 0
                self.player = AStar(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self.goal_state, self, "Uniform")
                self.dashboard = AStarDashboard(self.screen)
            case "Greedy":
                settings.WEIGHT = 1
                settings.G = 0
                settings.H = 1
                self.player = AStar(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self.goal_state, self, "Greedy")
                self.dashboard = AStarDashboard(self.screen)
            case "Weighted A*":
                settings.WEIGHT = 3
                settings.G = 1
                settings.H = 1
                self.player = AStar(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self.goal_state, self, "Weighted A*")
                self.dashboard = AStarDashboard(self.screen)
            case "IDA*":
                self.player = IDAStar(position, './sprites/pawn.png', self.screen, self.tiles, self.entities, self.winningPositions, self.goal_state, self, "IDA*")
                self.dashboard = IDAStarDashboard(self.screen)
        
        self.moveLog.append((Position(self.player.position.x, self.player.position.y), entitiesStartingPos))

    def draw(self):

        """
            Draw the level
        """

        self.screen.fill((59, 61, 122))

        offset_x = (settings.WINDOW_SIZE[0] - self.width * 32 * settings.SCALE_FACTOR) / 2
        offset_y = (settings.WINDOW_SIZE[1] - self.height * 32 * settings.SCALE_FACTOR) / 2

        for tile in self.tiles:
            tile.draw((tile.position.x * tile.screenSize + offset_x, tile.position.y * tile.screenSize + offset_y))

        for entity in self.entities:
            entity.draw((entity.position.x * entity.screenSize + offset_x, entity.position.y * entity.screenSize + offset_y))
        
        self.player.draw((self.player.position.x * self.player.screenSize + offset_x, self.player.position.y * self.player.screenSize + offset_y))
        if (self.hint):
            self.screen.blit(self.sprite_hint, (self.hint.x * self.player.screenSize + offset_x, self.hint.y * self.player.screenSize + offset_y))

        self.dashboard.update()

    def update(self):

        """
            Update the state of the game after each action of the player
        """

        action = self.player.update(self.dashboard)
        if action == "Move":
            self.hint = None
            if(self.player.move(self.tiles, self.entities)): 

                # Update the new positions after the move
                new_positions = []
                for entity in self.entities:
                    new_positions.append(Position(entity.position.x, entity.position.y))

                self.moveLog.append((Position(self.player.position.x, self.player.position.y), new_positions))
                self.dashboard.nrMoves += 1

        if(action == "Undo"):
            self.hint = None
            if len(self.moveLog) > 1:
                # Pop current positions and update the entities to the previous positions
                self.moveLog.pop()

                (newP, newE) = self.moveLog[-1]
                for i in range (len(self.entities)):
                    self.entities[i].position = Position(newE[i].x, newE[i].y)
                self.player.position = Position(newP.x, newP.y)

                self.dashboard.nrMoves -= 1

        if(action == "Hint"):
            self.hint = self.player.hint(self.tiles, self.entities, self.winningPositions)

        self.gamewin = self.checkWinCondition()
        self.draw()
    
    def checkWinCondition(self):

        """
            Check if the game is won
        """

        white_to_black = {}
        black_knights = [knight for knight in self.entities if knight.color == "BLACK"]
        white_knights = [knight for knight in self.entities if knight.color == "WHITE"]
        
        for black_knight, checking_position in self.winningPositions:
            for white_knight in white_knights:
                if white_knight.position == checking_position:
                    if white_knight in white_to_black:
                        white_to_black[white_knight].append(black_knight)
                    else:
                        white_to_black[white_knight] = [black_knight]
        
        every_white_is_checking_a_black = True
        for white_knight in white_knights:
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
        
        

    def saveDashboard(self, levelId):

        """
            Save the game data in the JSON file
        """
        
        file_path = './data/dashboard.json'

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        game_data = {"level":levelId, "player": self.chosenPlayer, "time": self.dashboard.time, "moves": self.dashboard.nrMoves}

        data['dashboard'].append(game_data)

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
                
        