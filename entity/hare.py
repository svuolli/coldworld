import pygame
from random import randint, choice

from gameentity import GameEntity

SCREEN_SIZE = (1280, 720)
        
        
class Hare(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "hare", image)
        self.dead_image = pygame.transform.flip(image, 0, 1)
        self.health = 25
        self.max_speed = 50. + randint(-20, 20)
        
    def bitten(self):
        
        self.health -= 1
        if self.health <= 0:
            self.max_speed = 0.
            self.image = self.dead_image
        self.max_speed = 140.
        
    def render(self, surface, offset):
        
        GameEntity.render(self, surface, offset)
                
        x, y = self.location - offset
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h/2
        surface.fill( (255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill( (0, 255, 0), (bar_x, bar_y, self.health, 4))
        
    def process(self, time_passed):
        
        x, y = self.location
        if x > SCREEN_SIZE[0] + 2:
            self.world.remove_entity(self)
            return
        
        GameEntity.process(self, time_passed)
