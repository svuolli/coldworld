
import pygame
from pygame.locals import *
from random import randint, choice

from gameobjects.vector2 import Vector2

from gamestate import GameState
from world import World, Human, Grass, Hare

class InGameState(GameState):
    def __init__(self):
        self.world = World()

        self.human_red_image = pygame.image.load("images/human_red.png").convert_alpha()
        self.grass_image = pygame.image.load("images/grass.png").convert_alpha()
        self.hare_image = pygame.image.load("images/hare.png").convert_alpha()

        for human_count in xrange(1):
            human_red = Human(self.world, self.human_red_image)
            human_red.location = Vector2(randint(0, 640), randint(0, 480))
            self.world.add_entity(human_red)

        for grass_count in xrange(randint(6,10)):
            grass = Grass(self.world, self.grass_image)
            grass.location = Vector2(randint(0, 640), randint(0, 480))
            self.world.add_entity(grass)


    def onEvent(self, event):
        pass

    def update(self, passed_time, state_list):
        if randint(1, 100) == 1:
            hare = Hare(self.world, self.hare_image)
            hare.location = Vector2(-50, randint(0, 480))
            hare.destination = Vector2(640+50, randint(0, 480))            
            self.world.add_entity(hare)

        self.world.process(passed_time)

    def render(self, screen):
        self.world.render(screen)

