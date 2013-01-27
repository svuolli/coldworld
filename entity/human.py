import pygame, math
from gameobjects.vector2 import Vector2
from locals import *

from gameentity import GameEntity

player1Keys = {'UP':pygame.K_w, 'DOWN':pygame.K_s, 'LEFT':pygame.K_a, 'RIGHT':pygame.K_d }
player2Keys = {'UP':pygame.K_UP, 'DOWN':pygame.K_DOWN, 'LEFT':pygame.K_LEFT, 'RIGHT':pygame.K_RIGHT }
player3Keys = {'UP':pygame.K_UP, 'DOWN':pygame.K_DOWN, 'LEFT':pygame.K_LEFT, 'RIGHT':pygame.K_RIGHT }
player4Keys = {'UP':pygame.K_UP, 'DOWN':pygame.K_DOWN, 'LEFT':pygame.K_LEFT, 'RIGHT':pygame.K_RIGHT }


players = {1:player1Keys, 2:player2Keys, 3:player3Keys, 4:player4Keys}

FRAME_TIME = 0.1

def loadImage(filename):
    return pygame.image.load(filename).convert_alpha()
    
class Human(GameEntity):
    
    def __init__(self, world, playernumber):
        
        GameEntity.__init__(self, world, "human_red", None)

        fmt = "images/davy%i.png" if playernumber == 1 else "images/aslak%i.png"
        image_files = map(lambda i: fmt%(i+1), xrange(2))
        self.images_lf = map(lambda f: loadImage(f), image_files)
        self.images_rf = map(lambda i: pygame.transform.flip(i, 1, 0), self.images_lf)

        self.current_frame = 0
        self.frame_timer = FRAME_TIME
        self.left_facing = False

        self.carry_image = None
        self.max_speed = 180.        
        self.player_number = playernumber

        self.hunger = 100.0
        self.hunger_image_index = 0
        self.thirst = 100.0
        self.thirst_image_index = 0
        self.heat = 100.0
        self.heat_image_index = 0

        self.age = 0.0

        self.sounds = {"walk":pygame.mixer.Sound("audio/running_in_snow.wav"),
                "eat":pygame.mixer.Sound("audio/eat.wav"),
                }
        
        self.x_heading = 0
        self.y_heading = 0

        if(pygame.joystick.get_count() > self.world.joystick_in_use):
            self.setup_joystick()
        else:
            self.joycontrol = -1
            self.init_keymap(self.player_number)

    def setup_joystick(self):
        joy_n = self.world.joystick_in_use
        self.joycontrol = joy_n
        self.joystick = pygame.joystick.Joystick(joy_n)
        self.joystick.init()
        self.world.joystick_in_use +=1

    def start_walking_sound(self):
        self.sounds["walk"].play(-1)
        
    def stop_walking_sound(self):
        self.sounds["walk"].stop()
        
    def init_keymap(self, player_number_):
    
        self.key_map = {
            players[self.player_number]['LEFT']: (-1, 0),
            players[self.player_number]['RIGHT']: (1, 0),
            players[self.player_number]['UP']: (0, -1),
            players[self.player_number]['DOWN']: (0, 1)
        }
        
    def carry(self, image):
        
        self.carry_image = image
        
    def drop(self, surface, offset):
        
        if self.carry_image:
            x, y = self.location - offset
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w/2, y-h))
            self.carry_image = None
        
    def render(self, surface, offset):
        current_frame = self.current_frame
        image = self.images_lf[current_frame] if self.left_facing else self.images_rf[current_frame]
        x, y = self.location - offset
        w, h = image.get_size()
        surface.blit(image, (x-w/2, y-h))
            
    def process(self, time_passed):
        self.hunger -= time_passed*2.5
        self.thirst -= time_passed*2.5
        self.heat -= time_passed*2.5
        self.age += time_passed
    
        pressed = pygame.key.get_pressed()
        move_vector = (0, 0)
        if(self.joycontrol == -1):
            for m in (self.key_map[key] for key in self.key_map if pressed[key]):
                move_vector = map(sum, zip(move_vector, m))
        else:
            x = self.joystick.get_axis(0)
            y = self.joystick.get_axis(1)

            if math.fabs(x) < 0.1:
                x = 0.
            if math.fabs(y) < 0.1:
                y = 0.
                
            move_vector = Vector2(x,y)
            

        self.heading = Vector2(move_vector)
        if move_vector[0] < 0.0:
            self.left_facing = True
        elif move_vector[0] > 0.0:
            self.left_facing = False

        if self.heading.get_length() > 0.0:
            self.frame_timer -= time_passed
            if self.frame_timer < 0.0:
                self.frame_timer = FRAME_TIME
                self.current_frame += 1
                if self.current_frame >= len(self.images_rf):
                    self.current_frame = 0
    
        GameEntity.process(self, time_passed)
        hare = self.world.get_close_entity("hare", self.location, 80)
        if hare:
            self.hunger = min(self.hunger+20.0, 120.0)
            self.world.remove_entity(hare)
            self.world.hare_count -= 1
            self.sounds["eat"].play()
        fire = self.world.get_close_entity("fire", self.location, 80)
        if fire:
            self.heat = min(self.heat+time_passed*20.0, 120)
        water = self.world.get_close_entity("water", self.location, 80)
        if water:
            self.thirst = min(self.thirst+time_passed*20.0, 120)

        if self.hunger < 0.0 or self.heat < 0.0 or self.thirst < 0.0:
            self.world.remove_entity(self)
            self.world.human_count -= 1
        
        self.hunger_image_index = min(5,int(6.0*self.hunger/120.0))
        self.thirst_image_index = min(5,int(6.0*self.thirst/120.0))
        self.heat_image_index = min(5,int(6.0*self.heat/120.0))
