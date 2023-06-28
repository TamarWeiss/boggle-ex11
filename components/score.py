from tkinter import Widget, Label, TOP

from components.var_label import VarLabel
from consts import FONT, FONTSIZE, PAD

class Score(VarLabel):
    """A component tasked with keeping track of the game's score"""

    def __init__(self):
        super().__init__(0)

    def pack_result(self, root: Widget):
        Label(root, text=f'Final Score: {self.get()}', font=(FONT, FONTSIZE), pady=PAD / 2).pack(side=TOP)

    def pack(self, root: Widget):
        super().pack(root, 'Score:', col=1)

    def add(self, score: int) -> int:
        return self.set(self.get() + score)