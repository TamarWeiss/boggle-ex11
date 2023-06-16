from tkinter import Widget, Label

from components.var_label import VarLabel
from consts import FULL_FONT

class Score(VarLabel):
    def __init__(self):
        super().__init__(0)

    def pack_result(self, root: Widget):
        Label(root, text=f'Final Score: {self.get()}', font=FULL_FONT, pady=5).pack(side='top')

    def pack(self, root: Widget, text='Score:'):
        super().pack(root, 'Score:', 1)

    def add(self, score: int) -> int:
        score = self.get() + score
        return self.set(score)