import pygame
from pygame import Surface

from src.utils.position import Position
import settings

class Entity:

    def __init__(self, position : Position, sprite, screen: Surface):
        self.position = position
        # self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite), (32 * settings.SCALE_FACTOR, 32 * settings.SCALE_FACTOR))
        self.screen = screen
        self.screenSize = 32 * settings.SCALE_FACTOR
        self.previousPosition = Position(position.x, position.y)

    def draw(self, coords):
        """
            Draw the entity on the screen
        """
        self.screen.blit(self.sprite, coords)

    def move(self, direction):
        
        """
            Move the entity to a new position
        """

        self.previousPosition = Position(self.position.x, self.position.y)
        self.position = Position(self.position.x + direction.x, self.position.y + direction.y)