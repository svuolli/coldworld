from gameentity import GameEntity

class Block(GameEntity):
    
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "block", image)

    def render(self, surface, offset):
        image = self.image
        x, y = self.location - offset
        w, h = image.get_size()
        surface.blit(image, (x-w/2, y-h))
