from tkinter import Label, Widget, Variable
from typing import Optional

from consts import FONT, FONTSIZE, PAD

class VarLabel:
    def __init__(self, value=''):
        self.root: Optional[Widget] = None
        self.var = Variable(value=value)
        self.__init_value = value

    def pack(self, root: Widget, text: str, col=0, var: Variable = None):
        self.root = root
        var = var or self.var

        Label(root, text=text, font=(FONT, FONTSIZE - 2)).grid(row=0, column=2 * col, sticky='e')
        Label(root, textvariable=var, font=(FONT, FONTSIZE - 2)).grid(
            row=0, column=2 * col + 1, padx=PAD / 2, sticky='w'
        )

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)
        return value

    def reset(self):
        self.var.set(self.__init_value)