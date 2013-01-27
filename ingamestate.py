
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
from entity.water import Water
from viewport import Viewport
from AudioSystem import MusicPlayer

ground_tile_fmt = "images/ground%i.png"
ground_tiles = map(lambda i: ground_tile_fmt % (i+1), xrange(6))

from endstate import EndState

class InGameState(GameState):
    def __init__(self):
        self.done = False
        self.world = World()

        self.ambient = pygame.mixer.Sound("audio/generic_ambient1.wav")        
        self.ambient.play(-1)
        
        self.fire_images = []
        self.hare_images_rf = []
        self.water_images = []

        self.player = MusicPlayer()       
        self.wait_for_song = 1200
        self.music_playing = False

        self.hare_timer = 1.0
        self.hare_timer_add = 1.0
        
        self.fire_timer = 1.0
        self.fire_timer_add = 1.0

        for i in xrange(3):
            filename = "images/fire%i.png" % (i+1)
            image = pygame.image.load(filename).convert_alpha()
            self.fire_images.append(image)

        for i in xrange(2):
            filename = "images/hare%i.png" % (i+1)
            image = pygame.image.load(filename).convert_alpha()
            self.hare_images_rf.append(image)

        for i in xrange(2):
            filename = "images/water%i.png" % (i+1)
            image = pygame.image.load(filename).convert_alpha()
            self.water_images.append(image)

        self.hare_images_lf = map(lambda i: pygame.transform.flip(i, 1, 0), self.hare_images_rf)

        self.humans = []
        self.viewports = []

        for human_count in xrange(2):
            human_red = Human(self.world, human_count+1)
            human_red.location = self.get_safe_spot()
            self.world.add_entity(human_red)
            self.humans.append(human_red)
            offset = human_count*SCREEN_SIZE[0]/2+1
            r = pygame.Rect(offset, 0, SCREEN_SIZE[0]/2-1, SCREEN_SIZE[1])
            viewport = Viewport(r, human_red)
            self.viewports.append(viewport)

        for fire_count in xrange(randint(10,50)):
            fire = Fire(self.world, self.fire_images)
            fire.location = self.get_safe_spot()
            self.world.add_entity(fire)
            self.world.fire_count += 1

        for water_count in xrange(randint(5, 10)):
            water = Water(self.world, self.water_images)
            water.location = self.get_safe_spot()
            self.world.add_entity(water)
            self.world.hare_count += 1

    def onEvent(self, event):
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
            self.done = True
        if event.type == AudioSystem.SONG_END:
            self.music_playing = False
            
    def get_safe_spot(self):
        while True:
            p = (randint(1, WORLD_SIZE[0]-1), randint(1, WORLD_SIZE[1]-1))
            if not self.world.grid.getBlock(p[0], p[1]):
                return Vector2(p[0], p[1]) * BLOCK_SIZE

    def update(self, passed_time, state_list):
        if self.world.human_count < 1:
            done = True
            state_list.pop()
            state_list.append(EndState(self.humans[0].age, self.humans[1].age))
            return
        if self.done:
            state_list.pop()
            return

        distance_of_humans = self.humans[0].location.get_distance_to(self.humans[1].location)
        if distance_of_humans < 40:
            hunger = self.humans[0].hunger + self.humans[1].hunger
            thirst = self.humans[0].thirst + self.humans[1].thirst
            heat = self.humans[0].heat + self.humans[1].heat
            for h in self.humans:
                h.hunger = hunger / 2.0
                h.thirst = thirst / 2.0
                h.heat = heat / 2.0

        if self.world.hare_count < 30:
            self.hare_timer -= passed_time

        if self.hare_timer < 0.0:
            hare = Hare(self.world, self.hare_images_lf, self.hare_images_rf)
            hare.location = self.get_safe_spot()
            hare.heading = choice([Vector2(1, 0), Vector2(-1, 0), Vector2(0, -1), Vector2(0, 1)])
            self.world.add_entity(hare)
            self.hare_timer = self.hare_timer_add
            self.hare_timer_add += randint(2, 5)
            self.world.hare_count += 1
            print "hare spawned"

        if self.world.fire_count < 30:
            self.fire_timer -= passed_time

        if self.fire_timer < 0.0:
            fire = Fire(self.world, self.fire_images)
            fire.location = self.get_safe_spot()
            self.world.add_entity(fire)
            self.world.fire_count += 1
            self.fire_timer = self.fire_timer_add
            self.fire_timer_add += randint(2, 5)
            print "fire spawned"

        if not self.music_playing:
            self.wait_for_song -= passed_time            
            if self.wait_for_song < 0.0:
                self.player.PlayTrack()
                self.music_playing = True
                self.wait_for_song = randint(5000, 20000)
                
        self.world.process(passed_time)

    def render(self, screen):
        for viewport in self.viewports:
            viewport.render(screen)
        for plr in xrange(2):
            x = plr*640 + 260
            y = 20
            screen.fill((0, 255, 0), (x, y+00, int(self.humans[plr].hunger), 10))
            screen.fill((0, 0, 255), (x, y+10, int(self.humans[plr].thirst), 10))
            screen.fill((255, 0, 0), (x, y+20, int(self.humans[plr].heat), 10))

