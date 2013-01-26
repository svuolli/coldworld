from gameobjects.vector2 import Vector2

from state.statemachine import StateMachine

class GameEntity(object):
    
    def __init__(self, world, name, image):
        
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.heading = Vector2(0, 0)
        self.max_speed = 0.
        
        self.brain = StateMachine()
        
        self.id = 0
        
    def pause(self):
    
        pass
        
    def render(self, surface, offset):
        
        x, y = self.location - offset
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h))

    def on_collide(self):
        pass
        
    def set_heading(self, heading_):
    
        self.heading = heading_
        
    def process(self, time_passed):
        
        self.brain.think()
        
        if self.heading.get_length() > 0:
            travel_distance = time_passed * self.max_speed
            self.move(self.heading.normalise() * time_passed * self.max_speed)
        
    def move(self, amount):
        new_pos = self.location + amount
        collide = self.world.grid.getBlock(int(new_pos.x/64), int(new_pos.y/64)) != None
        collide = collide or (self.world.grid.getBlock(int((new_pos.x-32)/64), int(new_pos.y/64)) != None)
        collide = collide or (self.world.grid.getBlock(int((new_pos.x)/64), int((new_pos.y-48)/64)) != None)
        collide = collide or (self.world.grid.getBlock(int((new_pos.x-32)/64), int((new_pos.y-48)/64)) != None)
        if collide:
            self.on_collide()
        else:
            self.location = new_pos
