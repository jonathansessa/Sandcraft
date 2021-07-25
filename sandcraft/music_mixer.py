from pygame import mixer

class MusicMixer:
    def __init__(self):
        self.__foundParticle = mixer.Sound("music/newParticle.wav")
        self.__foundParticle.set_volume(.05)
        self.__backgroundMusic = mixer.Sound("music/background.wav")
        self.__backgroundMusic.set_volume(.05)
        self.__solidSound = mixer.Sound("music/solidSound.wav")
        self.__solidSound.set_volume(.02)
        self.__liquidSound = mixer.Sound("music/liquidSound.wav")
        self.__liquidSound.set_volume(.02)
        self.__fixedSound = mixer.Sound("music/fixedSound.wav")
        self.__fixedSound.set_volume(.02)
        self.__playingEffect = False
        self.__partChannel = mixer.Channel(2)

        #channel for background music, particles, and ding_dingdiscovery
    
    def ding_discovery(self):
        self.__foundParticle.play()

    def play_particle_effect(self, partState):
        if not self.__partChannel.get_busy():
            if partState == "solid":
                self.__partChannel.play(self.__solidSound)
            if partState == "liquid":
                self.__partChannel.play(self.__liquidSound)
            if partState == "fixed":
                self.__partChannel.play(self.__fixedSound)

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

    
    