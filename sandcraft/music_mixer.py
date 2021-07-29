import os
from pygame import mixer

class MusicMixer:
    def __init__(self):
        mixer.init()
        self.__foundParticle = mixer.Sound(os.path.join(os.path.dirname(__file__), 'soundFiles', 'newParticle.wav'))
        self.__foundParticle.set_volume(.05)
        self.__backgroundMusic = mixer.Sound(os.path.join(os.path.dirname(__file__), 'soundFiles', 'background.wav'))
        self.__backgroundMusic.set_volume(.05)
        self.backgroundPlay()   
    
    def ding_Discovery(self):
        self.__foundParticle.play()

    def backgroundPlay(self):
        self.__backgroundMusic.play(-1)

    def change_volume_background(self, vol):
        self.__backgroundMusic.set_volume(vol)

    def endMixer(self):
        mixer.fadeout(1000)
        del self
