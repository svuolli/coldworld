SCREEN_SIZE = (1280, 720)

import pygame
from pygame.locals import *
from random import randint, choice

from gameobjects.vector2 import Vector2

from ingamestate import InGameState

def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    
    clock = pygame.time.Clock()

    state_list = [InGameState()]
    
    while len(state_list) > 0:
        current_state = state_list[-1]
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            else:
                current_state.onEvent(event)
        
        time_passed = clock.tick(30)
        current_state.update(time_passed, state_list)
        current_state.render(screen)
        
        pygame.display.update()
    
if __name__ == "__main__":    
    run()

