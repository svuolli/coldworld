
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
                if randint(0, 99) < 4:
                    x = cell * BLOCK_SIZE
                    block = Block(world, choice(self.images))
                    block.location = Vector2(x, y)
                    line.append(block)
                else:
                    line.append(None)
            self.grid.append(line)
   
    def getBlock(self, x, y):
       return self.grid[y][x]

    def render(self, line_num, surface, offset):
        start_index = min(int(offset.x) / BLOCK_SIZE, WORLD_SIZE[0])
        end_index = min(start_index + 12, WORLD_SIZE[0])
        line = self.grid[line_num]
        for cell in xrange(start_index, end_index):
            if line[cell]:
                line[cell].render(surface, offset)

