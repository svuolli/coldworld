from gameentity import GameEntity

class Grass(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "grass", image)
