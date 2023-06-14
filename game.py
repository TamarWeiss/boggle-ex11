import tkinter

from boggle_board_randomizer import randomize_board
from ex11_utils import Path, get_word

class Game:
    def __init__(self, width: int, height: int):
        self.__root = tkinter.Tk()
        self.width = width
        self.height = height
        self.__score = tkinter.IntVar(value=0)

        self.__root.title('Boggle')
        self.__center(width, height)
        self.__init_title_screen()

    def __center(self, width: int, height: int, ):
        root = self.__root
        x = (root.winfo_screenwidth() - width) // 2
        y = (root.winfo_screenheight() - height) // 2

        root.geometry(f"{width}x{height}+{x}+{y}")
        root.minsize(width, height)

    def __clear(self):
        for widget in self.__root.winfo_children():
            widget.destroy()

    def __init_title_screen(self, end=False):
        self.__clear()
        frame = tkinter.Frame(self.__root)
        title = tkinter.Label(frame, text='Boggle' if not end else 'Game Over!', font=('sans serif', 30), pady=5)
        button = tkinter.Button(frame, text='Play' if not end else 'Restart', font=('sans serif', 20),
            command=self.__generate_board)

        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        title.pack(side=tkinter.TOP)

        if end:
            score = tkinter.Label(frame, text=f'Final Score: {self.__score.get()}', font=('sans serif', 20), pady=5)
            score.pack(side=tkinter.TOP)

        button.pack(side=tkinter.TOP, pady=10)

    def __init_score_frame(self):
        self.__time = tkinter.IntVar(value=60)
        FONT = ('sans serif', 20)

        frame = tkinter.Frame(self.__root)
        timer_label = tkinter.Label(frame, text='Time:', font=FONT)
        timer = tkinter.Label(frame, textvariable=self.__time, font=FONT)
        score_label = tkinter.Label(frame, text='Score:', font=FONT)
        score = tkinter.Label(frame, textvariable=self.__score, font=FONT)

        frame.pack(side='top', fill='x', padx=20, pady=10)
        timer_label.grid(row=0, column=0, sticky=tkinter.E)
        timer.grid(row=0, column=1, padx=5, sticky=tkinter.W)
        score_label.grid(row=0, column=2, sticky=tkinter.E)
        score.grid(row=0, column=3, padx=5, sticky=tkinter.W)

        for i in range(4):
            frame.columnconfigure(i, weight=1)
        self.__root.after(1000, self.count_down)

    def count_down(self):
        time = self.__time
        if time.get() > 0:
            time.set(self.__time.get() - 1)
            self.__root.after(1000, self.count_down)
        else:
            self.__init_title_screen(end=True)

    def __init_word_frame(self):
        self.__word = tkinter.StringVar()

        frame = tkinter.Frame(self.__root)
        frame.pack(side='bottom')
        label = tkinter.Label(frame, text='Word:', font=('sans serif', 18))
        word_label = tkinter.Label(frame, textvariable=self.__word, font=('sans serif', 18))

        label.pack(side='left', pady=10)
        word_label.pack(side='right', padx=5)

    def __generate_board(self):
        self.__clear()
        self.__init_score_frame()
        self.__content = tkinter.Frame(self.__root)
        self.__content.pack(fill='both', expand=True)
        self.__board = randomize_board()
        self.__path: Path = []

        for i, row in enumerate(self.__board):
            for j, cell in enumerate(row):
                button = tkinter.Button(self.__content, text=cell, font=("Courier", 25))
                button.bind('<Button-1>', self.__on_click)
                button.grid(row=i, column=j, padx=1, pady=1, sticky='nesw')
                self.__content.grid_columnconfigure(j, weight=1, uniform='button')
            self.__content.grid_rowconfigure(i, weight=1, uniform='1')
        self.__init_word_frame()

    def __on_click(self, e: tkinter.Event):
        path = self.__path
        button: tkinter.Button = e.widget
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

    def set_score(self, score: int):
        self.__score.set(score)

    def set_word(self):
        self.__word.set(get_word(self.__board, self.__path))

    def start(self):
        self.__root.mainloop()

if __name__ == "__main__":
    size = 500
    Game(size, size).start()