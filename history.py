from tkinter import Widget, font, Scrollbar, Label, Listbox

from consts import *
from list_var import ListVar


class History:
    def __init__(self):
        self.__history = ListVar()

    def pack(self, root: Widget):
        f = font.Font(font=(FONT, FONTSIZE - 2))
        f.configure(underline=True)
        label = Label(root, text='History', font=f)

        scrollbar = Scrollbar(root)
        history = Listbox(root,
                          yscrollcommand=scrollbar.set,
                          activestyle='none',
                          bg=OG,
                          selectbackground=OG,
                          selectforeground='black',
                          highlightthickness=0,
                          font=(FONT, FONTSIZE - 6),
                          listvariable=self.__history,
                          width=PADDING)
        scrollbar.config(command=history.yview)

        label.pack(pady=PADDING)
        history.pack(side='left', fill='y', pady=(0, PADDING))
        scrollbar.pack(side='right', fill='y', pady=(0, PADDING))

    def get(self) -> list[str]:
        return self.__history.get()

    def add(self, word: str):
        self.__history.append(word)

    def reset(self):
        self.__history.set([])