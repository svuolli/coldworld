import pygame
from random import randint, choice

from gameentity import GameEntity
from state.harestates import *

from locals import *

FRAME_TIME = 0.1
        
class Hare(GameEntity):
    
    def __init__(self, world, images_lf, images_rf):
        GameEntity.__init__(self, world, "hare", None)
        # self.dead_image = pygame.transform.flip(image, 0, 1)
        self.health = 25
        self.max_speed = 0
        self.current_frame = 0
        self.frame_timer = FRAME_TIME
        self.images_lf = images_lf
        self.images_rf = images_rf
        self.left_facing = False
        
        self.human_chasing = None
        self.amount_ran = 0.0
        
        exploring_state = HareStateExploring(self)
        fleeing_state = HareStateFleeing(self)
        
        self.brain.add_state(exploring_state)
        self.brain.add_state(fleeing_state)
        
        self.brain.set_state("exploring")
        
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
        
    def on_collide(self):
        old_heading = self.heading
        while old_heading == self.heading or self.heading.get_length == 0:
            self.heading = Vector2(randint(-1, 1), randint(-1, 1))

    def process(self, time_passed):
        self.frame_timer -= time_passed
        self.amount_ran += time_passed * self.max_speed
        if self.frame_timer < 0:
            self.frame_timer = FRAME_TIME
            self.current_frame += 1
            if self.current_frame >= len(self.images_lf) or self.current_frame >= len(self.images_rf):
                    self.current_frame = 0
        
        x, y = self.location
        
        GameEntity.process(self, time_passed)
        if self.heading.x < 0.0:
            self.left_facing = True
        elif self.heading.x > 0.0:
            self.left_facing = False
