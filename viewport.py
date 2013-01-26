import pygame
from pygame.locals import *

from gameobjects.vector2 import Vector2

class Viewport(object):
    def __init__(self, rect, entity):
        self.rect = rect
        self.entity = entity
        self.surface = pygame.Surface((rect.width, rect.height))

    def render(self, screen):
        offset = self.entity.location - Vector2(
                self.surface.get_width()/2,
                self.surface.get_height()/2)
                
        self.entity.world.render(self.surface, offset)
        screen.blit(self.surface, (self.rect.left, self.rect.top))

