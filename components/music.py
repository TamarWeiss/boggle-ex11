from pygame import mixer

DIR = 'sfx/'

def play(filename: str, loops=0, channel_num=0):
    mixer.init()
    sound = mixer.Sound(DIR + filename)
    sound.set_volume(0.25)
    mixer.Channel(channel_num).play(sound, loops)