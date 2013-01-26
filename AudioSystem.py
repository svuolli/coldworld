import pygame

class MusicPlayer:

    def __init__(self):
        self.tracks = ["audio/26.ogg"]

    def PlayTrack(self):
        pygame.mixer.music.load(self.tracks[0])
        pygame.mixer.music.play()
        
        
