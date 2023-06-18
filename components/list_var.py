from tkinter import Variable

class ListVar(Variable):
    """An extended Variable class which specialized with handling arrays"""

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