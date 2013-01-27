from state import State
from random import randint
from gameobjects.vector2 import Vector2


class HareStateExploring(State):
    
    def __init__(self, hare):
        
        State.__init__(self, "exploring")
        self.hare = hare
        
    def random_destination(self):
        
        old_heading = self.hare.heading
        
        while old_heading == self.hare.heading or self.hare.heading.get_length == 0:
          self.hare.heading = Vector2(randint(-1, 1), randint(-1, 1))    
    
    def do_actions(self):
        
        if randint(1, 50) == 1:
            self.random_destination()
            
    def check_conditions(self):
              
        close_human = self.hare.world.get_close_entity("human_red", self.hare.location, range=96.)
        if close_human != None and randint(0,100) > 50:
            self.hare.human_chasing = close_human
            return "fleeing"
        
        return None
    
    def entry_actions(self):
        
        self.hare.max_speed = 90. + randint(-10, 20)
        self.random_destination()
        
        
class HareStateFleeing(State):
    
    def __init__(self, hare):
        
        State.__init__(self, "fleeing")
        self.hare = hare
        self.started_running = False
    
    def check_conditions(self):
        
        if self.hare.amount_ran > 1800.0 or self.hare.human_chasing is None:
            self.hare.amount_ran = 0.0
            self.started_running = False
            self.hare.human_chasing = None
            return "exploring"
        
        return None
    
    def entry_actions(self):
    
        if self.hare.human_chasing is not None:                        
            if not self.started_running:
                self.hare.heading = self.hare.human_chasing.heading
                self.started_running = True
            self.hare.max_speed = 180. + randint(0, 20)
