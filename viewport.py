import pygame
from pygame.locals import *

class Viewport(object):
    def __init__(self, rect, entity):
        self.rect = rect
        self.entity = entity
        self.surface = pygame.Surface((rect.width, rect.height))

    def render(self, screen):
        self.entity.world.render(self.surface)
        screen.blit(self.surface, (self.rect.left, self.rect.top))

