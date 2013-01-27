
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

class EndState(GameState):
    def __init__(self, p1, p2):
        self.done = False
        self.image = pygame.image.load("images/game_over.png")
        w, h = self.image.get_size()
        x, y = ((1280-w)/2, (720-h)/2)
        self.pos = (x,y)

        self.font = pygame.font.SysFont("arial", 24)
        self.points = (p1, p2)
        fmt = "%s survived for %.2f seconds"
        names = ["Davy", "Aslak"]
        data = zip(names, self.points)

        texts = map(lambda d: fmt % (d[0], d[1]), data)
        color = (0,0,0)
        self.text_imgs = map(lambda t: self.font.render(t, False, color), texts)

    def onEvent(self, event):
        if event.type == KEYDOWN:
            self.done = True

    def update(self, time_passed, state_list):
        if self.done:
            state_list.pop()
            return

    def render(self, screen):
        screen.fill((255, 255, 255))
        
        screen.blit(self.image, self.pos)
        w, h = self.text_imgs[1].get_size()
        screen.blit(self.text_imgs[0], (20, 700-h))
        screen.blit(self.text_imgs[1], (1260-w, 700-h))

        # screen.blit(self.image, self.pos)
