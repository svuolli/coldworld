from gameobjects.vector2 import Vector2

from state.statemachine import StateMachine

class GameEntity(object):
    
    def __init__(self, world, name, image):
        
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.heading = Vector2(0, 0)
        self.previous_heading = Vector2(0, 0)
        self.max_speed = 0.
        
        self.brain = StateMachine()
        
        self.id = 0
        
    def pause(self):
    
        pass
        
    def render(self, surface, offset):
        
        x, y = self.location - offset
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))
        
    def set_heading(self, heading_):
    
        self.heading = heading_
        
    def start_walking_sound(self):
        pass
        
    def stop_walking_sound(self):
        pass
        
    def process(self, time_passed):
        
        self.brain.think()
        
        if self.heading.get_length() > 0:
        
            if self.previous_heading.get_length() == 0:
                self.start_walking_sound()
        
            if self.world.grid.getBlock(
                int(self.location[0] / 64 + self.heading[0]),
                int(self.location[1] / 64 + self.heading[1])
            ) == None:
                travel_distance = time_passed * self.max_speed
                self.move(self.heading.normalise() * time_passed * self.max_speed)
        
        elif self.previous_heading.get_length > 0:
            self.stop_walking_sound()
                
        self.previous_heading = self.heading
        
    def move(self, amount):
        
        self.location += amount
