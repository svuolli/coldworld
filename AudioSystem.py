import pygame
from random import choice

SONG_END = pygame.USEREVENT+1

class MusicPlayer:

    def __init__(self):
        self.tracks = [
                        "audio/26.ogg",
                        "audio/26evilheartbeat.ogg",
                        "audio/26jees_musiikkimainen.ogg",
                        "audio/26jeesjees.ogg",
                        "audio/26perusheartbeat.ogg"
                    ]
        pygame.mixer.music.set_endevent(SONG_END)           

    def PlayTrack(self):
        track = choice(self.tracks);
        print track
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
                
