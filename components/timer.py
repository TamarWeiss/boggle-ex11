from tkinter import StringVar, Widget
from typing import Callable

from components.music import play
from components.var_label import VarLabel
from consts import REFRESH_RATE

NEAR_END = 30
HURRY = 'hurry-up.mp3'

class Timer(VarLabel):
    def __init__(self, time: float):
        super().__init__(float(time))
        self.__time = StringVar(value=self.__format_time())
        self.var.trace_add('write', lambda *args: self.__time.set(self.__format_time()))

    def pack(self, root: Widget):
        super().pack(root, 'Time:', var=self.__time)

    def __substract(self) -> float:
        seconds = round(self.get() - REFRESH_RATE / 1000, 2)
        return self.set(seconds)

    def __format_time(self) -> str:
        seconds = self.get()
        return f'{int(seconds / 60)}:{str(round(seconds % 60, 2)).zfill(4)}'

    def count_down(self, callback: Callable):
        """Counts down the timer. If it's done, it calls the end screen."""
        seconds = self.__substract()
        if seconds > 0:
            seconds == NEAR_END and play(HURRY, channel_num=1)
            self.root.after(REFRESH_RATE, self.count_down, callback)
        else:
            callback()