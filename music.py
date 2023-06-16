from pygame import mixer

class Music:
    def __init__(self):
        mixer.init()
        self.__player = mixer.music

    def play(self, filename: str, loops=0):
        self.__player.load(filename)
        self.__player.play(loops)