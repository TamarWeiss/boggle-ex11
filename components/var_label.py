from tkinter import Label, Widget, Variable, E, W
from typing import Optional

from consts import FONT, FONTSIZE, PAD

class VarLabel:
    """A generic component with a given visual template, which helps keep track and modifiying a given variable"""

    def __init__(self, value=''):
        self.root: Optional[Widget] = None
        self.var = Variable(value=value)
        self.__init_value = value

    def pack(self, root: Widget, text: str, col=0, var: Variable = None):
        """The default look is of a static title label, and a dynamic variable label"""
        self.root = root
        var = var or self.var

        Label(root, text=text, font=(FONT, FONTSIZE - 2)).grid(row=0, column=2 * col, sticky=E)
        Label(root, textvariable=var, font=(FONT, FONTSIZE - 2)).grid(row=0, column=2 * col + 1, padx=PAD / 2, sticky=W)

    def get(self):
        return self.var.get()

    def set(self, value):
        """Updates the variable to the given value, and returns it"""
        self.var.set(value)
        return value

    def reset(self):
        """Resets the variable back to its initial value"""
        self.var.set(self.__init_value)