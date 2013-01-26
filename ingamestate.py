
import pygame
import AudioSystem
from pygame.locals import *
from random import randint, choice
from locals import *

from gameobjects.vector2 import Vector2

from gamestate import GameState
from world import World
from entity.human import Human
from entity.grass import Grass
from entity.hare import Hare
from entity.fire import Fire
from viewport import Viewport
from AudioSystem import MusicPlayer

ground_tile_fmt = "images/ground%i.png"
ground_tiles = map(lambda i: ground_tile_fmt % (i+1), xrange(6))

class InGameState(GameState):
    def __init__(self):
        self.done = False
        self.world = World()

        self.grass_image = pygame.image.load("images/grass.png").convert_alpha()
        self.hare_image = pygame.image.load("images/hare.png").convert_alpha()

        self.ambient = pygame.mixer.Sound("audio/generic_ambient1.wav")        
        self.ambient.play()
        
        self.fire_images = []
        self.hare_images_rf = []

        self.player = MusicPlayer()       
        self.wait_for_song = 12000
        self.music_playing = False
        
        for i in xrange(3):
            filename = "images/fire%i.png" % (i+1)
            image = pygame.image.load(filename).convert_alpha()
            self.fire_images.append(image)

        for i in xrange(2):
            filename = "images/hare%i.png" % (i+1)
            image = pygame.image.load(filename).convert_alpha()
            self.hare_images_rf.append(image)

        self.hare_images_lf = map(lambda i: pygame.transform.flip(i, 1, 0), self.hare_images_rf)

        self.humans = []
        self.viewports = []

        for human_count in xrange(2):
            human_red = Human(self.world, human_count+1)
            human_red.location = Vector2(randint(0, 640), randint(0, 480))
            self.world.add_entity(human_red)
            self.humans.append(human_red)
            offset = human_count*SCREEN_SIZE[0]/2+1
            r = pygame.Rect(offset, 0, SCREEN_SIZE[0]/2-1, SCREEN_SIZE[1])
            viewport = Viewport(r, human_red)
            self.viewports.append(viewport)

        for fire_count in xrange(randint(10,50)):
            fire = Fire(self.world, self.fire_images)
            fire.location = Vector2(randint(0, WORLD_SIZE[0]), randint(0, WORLD_SIZE[1])) * BLOCK_SIZE
            self.world.add_entity(fire)

    def onEvent(self, event):
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            self.done = True
        if event.type == AudioSystem.SONG_END:
            self.music_playing = False
            
            

    def update(self, passed_time, state_list):
        if self.done:
            state_list.pop()
            return

        if randint(1, 100) <= 2:
            hare = Hare(self.world, self.hare_images_lf, self.hare_images_rf)
            hare.location = Vector2(-50, randint(0, 480))
            hare.heading = Vector2(1, 0)            
            self.world.add_entity(hare)

        if not self.music_playing:
            self.wait_for_song -= passed_time
            if self.wait_for_song < 0.0:
                self.player.PlayTrack()
                self.music_playing = True
                self.wait_for_music = randint(5000,20000)
                
        self.world.process(passed_time)

    def render(self, screen):
        for viewport in self.viewports:
            viewport.render(screen)

