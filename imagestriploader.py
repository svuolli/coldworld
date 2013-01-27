import pygame
 
 
class ImageStripLoader(object):

    def __init__(self, filename):
    
        try:
            self.strip = pygame.image.load(filename).convert()
        except pygame.error:
            self.strip = None
            
    def image_from_coordinates(self, rectangle_):
    
        rectangle = pygame.Rect(rectangle_)
        image = pygame.Surface(rectangle.size).convert()
        image.blit(self.strip, (0, 0), rectangle)
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
        
    def images_from_coordinates(self, rectangles):
    
        return [self.image_from_coordinates(r) for r in rectangles]
