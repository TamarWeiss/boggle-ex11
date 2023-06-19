#the consatnts for our boggle game

SIZE = 500
TIME = 180

FONT = 'sans serif'
FONTSIZE = 18
PAD = 10

OG = 'SystemButtonFace'
RED = '#ff8080'
GREEN = '#afef8f'
BLUE = '#a6d9f2'

FAIL = 'honk.mp3'
SUCCESS = '1_up.wav'

FILENAME = 'boggle_dict.txt'

Board = list[list[str]]
Point = tuple[int, int]
Path = list[Point]
PathDict = dict[str, list[Path]]