import pygame

from gameobjects.vector2 import Vector2

from mapgrid import MapGrid
from locals import *
    
class World(object):
    
    def __init__(self):
        
        self.entities = {}
        self.entity_id = 0        
        self.background = pygame.surface.Surface(SPLIT_SCREEN_SIZE).convert()
        self.background.fill((255, 255, 255))
        self.grid = MapGrid(self)

        self.hare_count = 0
        self.fire_count = 0
        self.human_count = 2
        self.joystick_in_use = 0
        self.position_sorted = []
        for y in range(0, SCREEN_SIZE[1]):
            self.position_sorted.append([])
        
    def add_entity(self, entity):
        
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
        
    def remove_entity(self, entity):
        
        del self.entities[entity.id]
                
    def get(self, entity_id):
        
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
        
    def process(self, time_passed):
                
        time_passed_seconds = time_passed / 1000.0        
        for entity in self.entities.values():
            entity.process(time_passed_seconds)
            
    def render(self, surface, offset):
        surface.blit(self.background, (0, 0))

        start_line = min(int(offset.y/BLOCK_SIZE), WORLD_SIZE[1])
        last_line = min(start_line+13, WORLD_SIZE[1])
        for line in xrange(start_line, last_line):
            self.grid.render(line, surface, offset)
        
        entities_sorted = sorted(self.entities.values(), key=lambda entity: entity.location[1])
        
        for entity in entities_sorted:
            entity.render(surface, offset)
            
            
    def get_close_entity(self, name, location, range=100.):
        
        location = Vector2(*location)        
        
        for entity in self.entities.itervalues():            
            if entity.name == name:                
                distance = location.get_distance_to(entity.location)
                if distance < range:
                    return entity        
        return None
