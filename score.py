from tkinter import IntVar, Widget, Label

from consts import FONT, FONTSIZE, FULL_FONT


class Score:
    def __init__(self):
        self.__score = IntVar(value=0)

    def pack_result(self, root: Widget):
        Label(root, text=f'Final Score: {self.__score.get()}', font=FULL_FONT, pady=5).pack(side='top')

    def pack(self, root: Widget):
        Label(root, text='Score', font=(FONT, FONTSIZE - 2)).grid(row=0, column=2, sticky='e')
        Label(root, textvariable=self.__score, font=(FONT, FONTSIZE - 2)).grid(row=0, column=3, padx=5, sticky='w')

    def reset(self):
        self.__score.set(0)

    def get(self) -> int:
        return self.__score.get()

    def add(self, score: int) -> int:
        score = self.get() + score
        self.__score.set(score)
        return score