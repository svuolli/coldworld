SCREEN_SIZE = (640, 480)

import pygame
from pygame.locals import *
from random import randint, choice

from gameobjects.vector2 import Vector2

from world import World, Human, Grass, Hare

def run():
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    
    world = World()
    
    w, h = SCREEN_SIZE
    
    clock = pygame.time.Clock()
    
    human_red_image = pygame.image.load("human_red.png").convert_alpha()
    grass_image = pygame.image.load("grass.png").convert_alpha()
    hare_image = pygame.image.load("hare.png").convert_alpha()
    
    for human_count in xrange(1):
        
        human_red = Human(world, human_red_image)
        human_red.location = Vector2(randint(0, w), randint(0, h))
        world.add_entity(human_red)
        
        
    for grass_count in xrange(randint(6,10)):
        grass = Grass(world, grass_image)
        grass.location = Vector2(randint(0, w), randint(0, h))
        world.add_entity(grass)
    
    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return        
        
        time_passed = clock.tick(30)
            
        if randint(1, 100) == 1:
            hare = Hare(world, hare_image)
            hare.location = Vector2(-50, randint(0, h))
            hare.destination = Vector2(w+50, randint(0, h))            
            world.add_entity(hare)
        
        world.process(time_passed)
        world.render(screen)
        
        pygame.display.update()
    
if __name__ == "__main__":    
    run()

