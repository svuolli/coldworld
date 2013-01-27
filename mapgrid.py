
from locals import *
from random import choice, randint

import pygame

from gameobjects.vector2 import Vector2

from entity.block import Block

def loadImage(filename):
    return pygame.image.load(filename).convert_alpha()

class MapGrid(object):
    def __init__(self, world):
        self.grid = []
        self.images = map(lambda f: loadImage("images/" + f), [
            "tree1.png",
            "tree2.png",
            "tree3.png",
            "tree4.png"])
        print self.images

        for line_num in xrange(WORLD_SIZE[1]):
            line = []
            y = line_num * BLOCK_SIZE
            for cell in xrange(WORLD_SIZE[0]):
                on_edge = False
                if cell==0 or cell==WORLD_SIZE[0]-1:
                    on_edge = True
                if line_num==0 or line_num==WORLD_SIZE[1]-1:
                    on_edge = True

                if on_edge or randint(0, 99) < 5:
                    x = cell * BLOCK_SIZE
                    block = Block(world, choice(self.images))
                    image_size = block.image.get_size()
                    block.location = Vector2(x+image_size[0]/2, y+BLOCK_SIZE)
                    line.append(block)
                else:
                    line.append(None)
            self.grid.append(line)
   
    def getBlock(self, x, y):
        if x<0 or x>=WORLD_SIZE[0] or y<0 or y>=WORLD_SIZE[1]:
            return None
        return self.grid[y][x]

    def render(self, line_num, surface, offset):
        start_index = min(int(offset.x) / BLOCK_SIZE, WORLD_SIZE[0])
        end_index = min(start_index + 12, WORLD_SIZE[0])
        line = self.grid[line_num]
        for cell in xrange(start_index, end_index):
            if line[cell]:
                line[cell].render(surface, offset)

