from pygame import mixer

class Music:
    def __init__(self):
        mixer.init()

    @staticmethod
    def play(filename: str, loops=0, channel_num=0):
        sound = mixer.Sound('sfx/' + filename)
        sound.set_volume(0.5)
        mixer.Channel(channel_num).play(sound, loops)