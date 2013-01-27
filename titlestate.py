
import pygame
import AudioSystem
from pygame.locals import *
from random import randint, choice
from locals import *

from gameobjects.vector2 import Vector2

from gamestate import GameState
from world import World
from entity.human import Human
from entity.grass import Grass
from entity.hare import Hare
from entity.fire import Fire
from entity.water import Water
from viewport import Viewport
from AudioSystem import MusicPlayer

from ingamestate import InGameState

class TitleState(GameState):
    def __init__(self):
        self.done = False
        self.image = pygame.image.load("images/title_screen.png")
        w, h = self.image.get_size()
        x, y = ((1280-w)/2, (720-h)/2)
        self.pos = (x,y)
        self.start_game = False

    def onEvent(self, event):
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            self.done = True
        elif event.type == KEYDOWN and event.key == pygame.K_SPACE:
            self.start_game = True

    def update(self, time_passed, state_list):
        if self.done:
            state_list.pop()
            return
        if self.start_game:
            self.start_game = False
            state_list.append(InGameState())

    def render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.image, self.pos)
