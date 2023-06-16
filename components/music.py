from pygame import mixer

class Music:
    def __init__(self):
        mixer.init()

    @staticmethod
    def play(filename: str, loops=0, channel_num=0):
        mixer.Channel(channel_num).play(mixer.Sound(filename), loops)