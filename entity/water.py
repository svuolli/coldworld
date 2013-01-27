import pygame
from gameobjects.vector2 import Vector2

from random import randint

from gameentity import GameEntity

FRAME_TIME = 0.2

class Water(GameEntity):
    def __init__(self, world, images):
        GameEntity.__init__(self, world, "water", None)
        self.images = images
        self.current_frame = randint(0,1)
        self.frame_timer = randint(0, 100)/100.0

    def render(self, surface, offset):
        image = self.images[self.current_frame]
        x, y = self.location - offset
        w, h = image.get_size()
        surface.blit(self.images[self.current_frame], (x-w/2, y-h))

    def process(self, time_passed):
        self.frame_timer -= time_passed
        
        if self.frame_timer < 0:
            self.frame_timer = FRAME_TIME
            self.current_frame += 1
            if(self.current_frame >= len(self.images)):
                self.current_frame = 0
