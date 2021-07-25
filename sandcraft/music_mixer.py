from pygame import mixer

class MusicMixer:
    def __init__(self):
        self.__foundParticle = mixer.Sound("music/newParticle.wav")
        self.__foundParticle.set_volume(.05)
        self.__backgroundMusic = mixer.Sound("music/background.wav")
        self.__backgroundMusic.set_volume(.05)
        self.__solidSound = mixer.Sound("music/solidSound.wav")
        self.__solidSound.set_volume(.01)
        self.__liquidSound = mixer.Sound("music/liquidSound.wav")
        self.__liquidSound.set_volume(.03)
        self.__fixedSound = mixer.Sound("music/fixedSound.wav")
        self.__fixedSound.set_volume(.03)
        self.__playingEffect = False
        self.__solidChannel = mixer.Channel(2)
        self.__liquidChannel = mixer.Channel(3)
        self.__fixedChannel = mixer.Channel(4)
        #self.__gasChannel = mixer.Channel(5)
    
    def ding_discovery(self):
        self.__foundParticle.play()

    def play_particle_effect(self, partState):
        if partState == "solid" and not self.__solidChannel.get_busy():
            self.__solidChannel.play(self.__solidSound)
        if partState == "liquid"and not self.__liquidChannel.get_busy():
            self.__liquidChannel.play(self.__liquidSound)
        if partState == "fixed"and not self.__fixedChannel.get_busy():
            self.__fixedChannel.play(self.__fixedSound)

    def play_background(self):
            self.__backgroundMusic.play(-1)
            self.__playingBackground = True

    def change_volume_background(self, vol):
        self.__backgroundMusic.set_volume(vol)
    
    def fade_mixer(self):
        del self.__foundParticle
        del self.__solidSound
        del self.__fixedSound
        del self.__liquidSound
        mixer.fadeout(1500)

    
    