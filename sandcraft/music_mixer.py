import os
from pygame import mixer


class MusicMixer:
    def __init__(self):
        mixer.init()
        print(os.path.join(os.path.dirname(__file__), 'soundFiles', 'newParticle.wav'))
        self.__foundParticle = mixer.Sound(os.path.join(os.path.dirname(__file__), 'soundFiles', 'newParticle.wav'))
        self.__foundParticle.set_volume(.05)
        # self.__backgroundMusic = mixer.Sound("music/background.wav")
        # self.__backgroundMusic.set_volume(.05)
        # self.backgroundPlay()

    def ding_Discovery(self):
        self.__foundParticle.play()

    # def backgroundPlay(self):
    #    self.__backgroundMusic.play(-1)
