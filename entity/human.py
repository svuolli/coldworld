import pygame
from gameobjects.vector2 import Vector2

from gameentity import GameEntity

player1Keys = {'UP':pygame.K_UP, 'DOWN':pygame.K_DOWN, 'LEFT':pygame.K_LEFT, 'RIGHT':pygame.K_RIGHT }
player2Keys = {'UP':pygame.K_w, 'DOWN':pygame.K_s, 'LEFT':pygame.K_a, 'RIGHT':pygame.K_d }
player3Keys = {'UP':pygame.K_UP, 'DOWN':pygame.K_DOWN, 'LEFT':pygame.K_LEFT, 'RIGHT':pygame.K_RIGHT }
player4Keys = {'UP':pygame.K_UP, 'DOWN':pygame.K_DOWN, 'LEFT':pygame.K_LEFT, 'RIGHT':pygame.K_RIGHT }

players = {1:player1Keys, 2:player2Keys, 3:player3Keys, 4:player4Keys}
    
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
            players[self.player_number]['LEFT']: (-1, 0),
            players[self.player_number]['RIGHT']: (1, 0),
            players[self.player_number]['UP']: (0, -1),
            players[self.player_number]['DOWN']: (0, 1)
        }
        
    def carry(self, image):
        
        self.carry_image = image
        
    def drop(self, surface):
        
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))
            self.carry_image = None
        
    def render(self, surface):
        
        GameEntity.render(self, surface)
        
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))
            
    def process(self, time_passed):
    
        pressed = pygame.key.get_pressed()
        move_vector = (0, 0)
        for m in (self.key_map[key] for key in self.key_map if pressed[key]):
            move_vector = map(sum, zip(move_vector, m))
                    
        self.heading = Vector2(move_vector)
    
        GameEntity.process(self, time_passed)
