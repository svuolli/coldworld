import pygame
 
 
class imagestriploader(object):

    def __init__(self, filename):
    
        try:
            self.strip = pygame.image.load(filename).convert()
        except pygame.error:
            self.strip = None
            
    def image_from_coordinates(self, rectangle_):
    
        rectangle = pygame.Rect(rectangle_)
        image = pygame.Surface(rectangle.size).convert()
        image.blit(self.strip, (0, 0), rectangle)
        return image
        
    def images_from_coordinates(self, rectangles):
    
        return [self.image_from_coordinates(rectangle) for r in rectangles]
