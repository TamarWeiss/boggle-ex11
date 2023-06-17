from tkinter import Widget, font, Scrollbar, Label, Listbox

from components.list_var import ListVar
from components.var_label import VarLabel
from consts import FONTSIZE, FONT, PAD, OG

class History(VarLabel):
    """A component tasked with keeping track and displaying already found words"""

    def __init__(self):
        super().__init__()
        self.var = ListVar()

    def pack(self, root: Widget):
        f = font.Font(font=(FONT, FONTSIZE - 2))
        f.configure(underline=True)
        Label(root, text='History', font=f).pack(pady=PAD)

        scrollbar = Scrollbar(root)
        history = Listbox(root,
                          yscrollcommand=scrollbar.set,
                          activestyle='none',
                          bg=OG,
                          selectbackground=OG,
                          selectforeground='black',
                          highlightthickness=0,
                          font=(FONT, FONTSIZE - 6),
                          listvariable=self.var,
                          width=PAD)
        scrollbar.config(command=history.yview)

        history.pack(side='left', fill='y', pady=(0, PAD))
        scrollbar.pack(side='right', fill='y', pady=(0, PAD))

    def add(self, word: str):
        self.var.append(word)