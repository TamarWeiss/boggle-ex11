from tkinter import Widget, Label

from components.var_label import VarLabel
from consts import FONT, FONTSIZE

class Score(VarLabel):
    """A component tasked with keeping track of the game's score"""

    def __init__(self):
        super().__init__(0)

    def pack_result(self, root: Widget):
        Label(root, text=f'Final Score: {self.get()}', font=(FONT, FONTSIZE), pady=5).pack(side='top')

    def pack(self, root: Widget):
        super().pack(root, 'Score:', 1)

    def add(self, score: int) -> int:
        score = self.get() + score
        return self.set(score)