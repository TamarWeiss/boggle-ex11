from tkinter import DoubleVar, Label, StringVar, Widget
from typing import Callable, Optional

from consts import FONT, FONTSIZE, REFRESH_RATE
from music import Music

TIME = 180
NEAR_END = 30
HURRY = 'hurry-up.mp3'

class Timer:
    def __init__(self):
        self.__root: Optional[Widget] = None
        self.__music = Music()
        self.__seconds = DoubleVar(value=TIME)
        self.__time = StringVar(value=self.__format_time())
        self.__seconds.trace_add('write', lambda *args: self.__time.set(self.__format_time()))

    def pack(self, root: Widget):
        self.__root = root
        label = Label(root, text='Time:', font=(FONT, FONTSIZE - 2))
        timer = Label(root, textvariable=self.__time, font=(FONT, FONTSIZE - 2))

        label.grid(row=0, column=0, sticky='e')
        timer.grid(row=0, column=1, padx=5, sticky='w')

    def __substract(self) -> float:
        seconds = round(self.__seconds.get() - REFRESH_RATE / 1000, 2)
        self.__seconds.set(seconds)
        return seconds

    def __format_time(self) -> str:
        seconds = self.__seconds.get()
        return f'{int(seconds / 60)}:{str(round(seconds % 60, 2)).zfill(4)}'

    def count_down(self, callback: Callable):
        """Counts down the timer. If it's done, it calls the end screen."""
        seconds = self.__substract()
        if seconds > 0:
            seconds == NEAR_END and self.__music.play(HURRY)
            self.__root.after(REFRESH_RATE, self.count_down, callback)
        else:
            callback()

    def reset(self):
        self.__seconds.set(TIME)