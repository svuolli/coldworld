import pygame

from gameobjects.vector2 import Vector2

from gameentity import GameEntity
   
    
class Human(GameEntity):
    
    def __init__(self, world, image):
        
        GameEntity.__init__(self, world, "human_red", image)
        
        self.carry_image = None
        
        self.max_speed = 50
        
        self.player_number = 1
    
        self.x_heading = 0
        self.y_heading = 0
        
        self.init_keymap(self.player_number)
        
    def init_keymap(self, player_number_):
    
        self.key_map = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1)
        }
        
    def carry(self, image):
        
        self.carry_image = image
        
    def drop(self, surface, offset):
        
        if self.carry_image:
            x, y = self.location - offset
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))
            self.carry_image = None
        
    def render(self, surface, offset):
        
        GameEntity.render(self, surface, offset)
        
        if self.carry_image:
            x, y = self.location - offset
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))
            
    def process(self, time_passed):
    
        pressed = pygame.key.get_pressed()
        move_vector = (0, 0)
        for m in (self.key_map[key] for key in self.key_map if pressed[key]):
            move_vector = map(sum, zip(move_vector, m))
                    
        self.heading = Vector2(move_vector)
    
        GameEntity.process(self, time_passed)
