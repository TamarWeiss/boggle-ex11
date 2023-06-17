from tkinter import *

from components.list_var import ListVar
from components.var_label import VarLabel
from consts import Board, Point
from ex11_utils import get_word

class Word(VarLabel):
    """A component tasked with displaying the current word"""

    def __init__(self):
        super().__init__()
        self.var = ListVar()
        self.__word = StringVar()
        self.board = []
        self.var.trace_add('write', lambda *args: self.__word.set(get_word(self.board, self.get())))

    def pack(self, root: Widget, board: Board):
        self.board = board
        super().pack(root, 'Word:', var=self.__word)

    def add(self, point: Point):
        self.var.append(point)

    def remove(self, point: Point):
        self.var.remove(point)