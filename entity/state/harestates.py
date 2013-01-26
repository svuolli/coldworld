from state import State

from gameobjects.vector2 import Vector2


class HareStateExploring(State):
    
    def __init__(self, hare):
        
        State.__init__(self, "exploring")
        self.hare = hare
        
    def random_destination(self):
        
        self.hare.heading = Vector2(randint(-1, 1), randint(-1, 1))    
    
    def do_actions(self):
        
        if randint(1, 50) == 1:
            self.random_destination()
            
    def check_conditions(self):
                        
        # check if player tries to catch
        
        return None
    
    def entry_actions(self):
        
        self.hare.speed = 60. + randint(-30, 30)
        self.random_destination()
        
        
class HareStateFleeing(State):
    
    def __init__(self, hare):
        
        State.__init__(self, "fleeing")
        self.hare = hare
        self.player_chasing = None
    
    def check_conditions(self):
        
        # check if player is still chasing
        
        return None
    
    def entry_actions(self):
    
        if self.player_chasing is not None:                        
            self.hare.heading = Vector2(self.player_chasing[0] * -1, self.player_chasing[1] * -1)
            self.hare.speed = 90. + randint(5, 20)
