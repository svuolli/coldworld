import pygame
from random import randint, choice

from gameentity import GameEntity

from locals import *

FRAME_TIME = 0.2
        
class Hare(GameEntity):
    
    def __init__(self, world, images_lf, images_rf):
        GameEntity.__init__(self, world, "hare", None)
        # self.dead_image = pygame.transform.flip(image, 0, 1)
        self.health = 25
        self.max_speed = 80. + randint(-20, 20)
        self.current_frame = 0
        self.frame_timer = FRAME_TIME
        self.images_lf = images_lf
        self.images_rf = images_rf
        self.left_facing = False
        
    def bitten(self):
        
        self.health -= 1
        if self.health <= 0:
            self.max_speed = 0.
            #self.image = self.dead_image
        self.max_speed = 140.
        
    def render(self, surface, offset):
        current_frame = self.current_frame
        image = self.images_lf[current_frame] if self.left_facing else self.images_rf[current_frame]
        x, y = self.location - offset
        w, h = image.get_size()
        surface.blit(image, (x-w/2, y-h))
        
    def process(self, time_passed):
        self.frame_timer -= time_passed
        if self.frame_timer < 0:
            self.frame_timer = FRAME_TIME
            self.current_frame += 1
            if self.current_frame >= len(self.images_lf) or self.current_frame >= len(self.images_rf):
                    self.current_frame = 0
        
        x, y = self.location
        if x > SCREEN_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        
        GameEntity.process(self, time_passed)
