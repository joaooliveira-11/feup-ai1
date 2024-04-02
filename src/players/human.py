from typing import List
import pygame
import sys
from src.models.entity import Entity

from src.models.player import Player
from src.utils.position import Position
from src.entities.tile import Tile
from src.players.ai.IDdfs import IDDfs

class Human(Player):
    KEY_PRESS_EVENTS = {
        'down': pygame.USEREVENT + 1,
        'up': pygame.USEREVENT + 2,
        'left': pygame.USEREVENT + 3,
        'right': pygame.USEREVENT + 4,
        'space': pygame.USEREVENT + 5,
        'z': pygame.USEREVENT + 6,
    }

    def __init__(self, position, sprite, screen):
        super().__init__(position, sprite, screen)
    
    def update(self, dashboard):

        """
            Update the player's position based on the key pressed by the user
        """

        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                self.previousPosition = Position(self.position.x, self.position.y)
                if event.key == pygame.K_ESCAPE:
                    self.leave = True
                if event.key == pygame.K_DOWN:
                    self.position.y += 1
                    dashboard.key_states['down'] = True
                    pygame.time.set_timer(self.KEY_PRESS_EVENTS['down'], 100, True)
                    return "Move"
                if event.key == pygame.K_UP:
                    self.position.y -= 1
                    dashboard.key_states['up'] = True
                    pygame.time.set_timer(self.KEY_PRESS_EVENTS['up'], 100, True)
                    return "Move"
                if event.key == pygame.K_LEFT:
                    self.position.x -= 1
                    dashboard.key_states['left'] = True
                    pygame.time.set_timer(self.KEY_PRESS_EVENTS['left'], 100, True)
                    return "Move"
                if event.key == pygame.K_RIGHT:
                    self.position.x += 1
                    dashboard.key_states['right'] = True
                    pygame.time.set_timer(self.KEY_PRESS_EVENTS['right'], 100, True)
                    return "Move"
                if event.key == pygame.K_z:
                    dashboard.key_states['z'] = True
                    pygame.time.set_timer(self.KEY_PRESS_EVENTS['z'], 100, True)
                    return "Undo"
                if event.key == pygame.K_SPACE:
                    dashboard.key_states['space'] = True
                    pygame.time.set_timer(self.KEY_PRESS_EVENTS['space'], 100, True)
                    return "Hint"
            elif event.type in self.KEY_PRESS_EVENTS.values():
                for key, event_id in self.KEY_PRESS_EVENTS.items():
                    if event.type == event_id:
                        dashboard.key_states[key] = False
                        break
                    
    def move(self, tiles : List[Tile], entities : List[Entity]):

        """
            Move the player to the new position if it is a valid move or undo the move if it is not valid
        """

        direction = self.position - self.previousPosition
        
        for knight in entities:
            if self.position == knight.position and knight.color == "WHITE":
                next_knight_position = knight.position + direction
                if next_knight_position not in [knight.position for knight in entities] and next_knight_position in [tile.position for tile in tiles]: # Check if the next position is not occupied by another knight
                    knight.position = next_knight_position # Move the knight
                    self.previousPosition = self.position 
                    return True
                else:
                    self.position = self.previousPosition
                    return False
            if self.position == knight.position and knight.color == "BLACK":
                self.position = self.previousPosition
                return False
        
        # No collision with any knight
        if self.position in [tile.position for tile in tiles] and self.position != self.previousPosition: # Valid move on the board
            self.previousPosition = self.position
            return True
        else:
            self.position = self.previousPosition
            return False

    def hint(self, tiles, entities, winnning_positions):

        """
            Get a hint for the player
            Currently, the hint is implemented using the IDDFS algorithm
        """
        
        idfs = IDDfs(Position(self.position.x, self.position.y), './sprites/pawn.png', self.screen, tiles, entities, winnning_positions, 0, "IDDFS", True)
        path = idfs.path
        hint = path[0]
        return Position(hint.playerPosition[0], hint.playerPosition[1])