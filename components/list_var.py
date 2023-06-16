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
        var = self.get()
        var.remove(value)
        self.set(var)

    def __getitem__(self, index: int):
        return self.get()[index]