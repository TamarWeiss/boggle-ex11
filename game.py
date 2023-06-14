from tkinter import *
from typing import Union

from boggle_board_randomizer import randomize_board
from ex11_utils import Path, get_word

class Game:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__time = IntVar(value=60)
        self.__score = IntVar(value=0)

        self.__root.title('Boggle')
        self.__center(width, height)
        self.__init_title_screen()

    def __center(self, width: int, height: int):
        """Adjusts the window to the center of the screen"""
        root = self.__root
        x = (root.winfo_screenwidth() - width) // 2
        y = (root.winfo_screenheight() - height) // 2

        root.geometry(f"{width}x{height}+{x}+{y}")
        root.minsize(width, height)

    def __clear(self):
        """Will clear EVERYTHING in the main root"""
        for widget in self.__root.winfo_children():
            widget.destroy()

    def __init_title_screen(self, end=True):
        """Initialize the title screen of the game. Also doubles as the end screen if end boolean is set to True"""
        self.__clear()
        frame = Frame(self.__root)
        title = Label(frame, text='Boggle' if not end else 'Game Over!', font=('sans serif', 30), pady=5)
        button = Button(frame, text='Play' if not end else 'Restart', font=('sans serif', 20),
            command=self.__generate_board)

        frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        title.pack(side=TOP)
        if end:
            score = Label(frame, text=f'Final Score: {self.__score.get()}', font=('sans serif', 20), pady=5)
            score.pack(side=TOP)
        button.pack(side=TOP, pady=10)

    def __init_score_frame(self):
        self.__time.set(60)  # TODO: get initial seconds via a variable?
        self.__score.set(0)

        frame = Frame(self.__root)
        frame.pack(side='top', fill='x', padx=20, pady=10)
        self.init_var_label(frame, 'Time:', self.__time, 0)
        self.init_var_label(frame, 'Score:', self.__score, 1)

        for i in range(len(frame.children)):
            frame.columnconfigure(i, weight=1)
        self.__root.after(1000, self.count_down)

    def count_down(self):
        """Counts down the timer. If done, it calls the end screen."""
        time = self.__time
        if time.get() > 0:
            time.set(self.__time.get() - 1)
            self.__root.after(1000, self.count_down)
        else:
            self.__init_title_screen(end=True)

    def __init_word_frame(self):
        self.__word = StringVar()
        frame = Frame(self.__root, pady=10)
        frame.pack(side='bottom')
        self.init_var_label(frame, 'Word:', self.__word, 0, fontsize=18)

    @staticmethod
    def init_var_label(root: Widget, text: str, var: Union[IntVar, StringVar], i=0, fontsize=20):
        label = Label(root, text=text, font=('sans serif', fontsize))
        var_label = Label(root, textvariable=var, font=('sans serif', fontsize))
        label.grid(row=0, column=2 * i, sticky=E)
        var_label.grid(row=0, column=2 * i + 1, padx=5, sticky=W)

    def __generate_board(self):
        self.__clear()
        self.__init_score_frame()
        self.__content = Frame(self.__root)
        self.__content.pack(fill='both', expand=True)
        self.__board = randomize_board()
        self.__path: Path = []

        for i, row in enumerate(self.__board):
            for j, cell in enumerate(row):
                button = Button(self.__content, text=cell, font=("Courier", 25))
                button.bind('<Button-1>', self.__on_click)
                button.grid(row=i, column=j, padx=1, pady=1, sticky='nesw')
                self.__content.grid_columnconfigure(j, weight=1, uniform='button')
            self.__content.grid_rowconfigure(i, weight=1, uniform='1')
        self.__init_word_frame()

    def __on_click(self, e: Event):
        path = self.__path
        button: Button = e.widget
        grid_info = button.grid_info()
        point = (grid_info['row'], grid_info['column'])
        is_active = point in path

        if is_active:
            path.remove(point)
            button.configure(bg='SystemButtonFace')
        else:
            path.append(point)
            button.configure(bg='#b5d4e3')
        self.set_word()

    def add_score(self, score: int):
        self.__score.set(self.__score.get() + score)

    def set_word(self):
        self.__word.set(get_word(self.__board, self.__path))

    def start(self):
        self.__root.mainloop()

if __name__ == "__main__":
    size = 500
    Game(size, size).start()