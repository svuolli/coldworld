import pygame

SONG_END = pygame.USEREVENT+1

class MusicPlayer:

    def __init__(self):
        self.tracks = ["audio/26.ogg"]
        pygame.mixer.music.set_endevent(SONG_END)

    def PlayTrack(self):
        pygame.mixer.music.load(self.tracks[0])
        pygame.mixer.music.play()
        
        
