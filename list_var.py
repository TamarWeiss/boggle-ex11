from tkinter import Misc, Variable

class ListVar(Variable):
    def __init__(self, master: Misc = None, value=None, name: str = None):
        value = value or []
        super().__init__(master, value, name)

    def get(self) -> list:
        return list(super().get())

    def append(self, value):
        self.set(self.get() + [value])

    def remove(self, value):
        list_var = self.get()
        list_var.remove(value)
        self.set(list_var)

    def __getitem__(self, index: int):
        return self.get()[index]