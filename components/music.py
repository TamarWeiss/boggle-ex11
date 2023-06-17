from pygame import mixer

# The sfx directory
DIR = 'sfx/'

def play(filename: str, loops=0, channel_num=0, volume=0.25):
    """The game's audio player"""
    mixer.init()
    sound = mixer.Sound(DIR + filename)
    sound.set_volume(volume)
    mixer.Channel(channel_num).play(sound, loops)