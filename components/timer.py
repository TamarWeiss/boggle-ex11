from tkinter import StringVar, Widget
from typing import Callable

from components.music import play
from components.var_label import VarLabel

NEAR_END = 30
HURRY = 'hurry-up.mp3'
REFRESH_RATE = 100

class Timer(VarLabel):
    """A component tasked with keeping track of the remaining time. Will sound off an alert sfx when time is running out"""

    def __init__(self, time: float):
        super().__init__(float(time))
        self.__time = StringVar(value=self.__format_time())
        self.var.trace_add('write', lambda *args: self.__time.set(self.__format_time()))

    def pack(self, root: Widget, callback: Callable):
        super().pack(root, 'Time:', var=self.__time)
        self.root.after(REFRESH_RATE, lambda: self.__count_down(callback))

    def __format_time(self) -> str:
        """Format seconds into more suitable display format"""
        seconds = self.get()
        return f'{int(seconds / 60)}:{str(round(seconds % 60, 2)).zfill(4)}'

    def __count_down(self, callback: Callable):
        """Counts down the timer. If it's done, it'll call the end screen."""
        seconds = self.set(round(self.get() - REFRESH_RATE / 1000, 2))
        if seconds > 0:
            seconds == NEAR_END and play(HURRY, channel_num=1)
            self.root.after(REFRESH_RATE, self.__count_down, callback)
        else:
            callback()