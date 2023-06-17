from tkinter import *

from boggle_board_randomizer import randomize_board
from components.button import Button
from components.history import History
from components.music import play
from components.score import Score
from components.timer import Timer
from components.word import Word
from consts import *
from ex11_utils import is_valid_path, load_words

class Boggle:
    """A class which manages a boggle game"""

    def __init__(self, width: int, height: int):
        """Initialize the game variables, and call on the title screen"""
        self.__root = Tk()
        self.__words = load_words(FILENAME)
        self.__history = History()
        self.__timer = Timer(TIME)
        self.__score = Score()
        self.__word = Word()

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

    def start(self):
        """Starts the game"""
        self.__root.mainloop()

    # ---------------------------------------------------

    def __init_title_screen(self, end=False):
        """Initialize the title screen of the game. Also doubles as the end screen if end boolean is set to True"""
        self.__clear()
        self.__history.reset()
        self.__timer.reset()
        self.__word.reset()

        frame = Frame(self.__root)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(frame, text='Boggle' if not end else 'Game Over!', font=(FONT, FONTSIZE + 10), pady=5).pack(side='top')
        end and self.__score.pack_result(frame)
        Button(
            frame, text='Play' if not end else 'Restart', font=(FONT, FONTSIZE), command=self.__generate_board
        ).pack(side='top', pady=PAD)

    def __init_score(self):
        """Displays the score and time at the top of the window"""
        self.__score.reset()
        frame = Frame(self.__root)
        frame.pack(side='top', fill='x', padx=2 * PAD, pady=PAD)
        self.__score.pack(frame)
        self.__timer.pack(frame)

        # ensure the two labels resize at a constant rate.
        for i in range(len(frame.children)):
            frame.columnconfigure(i, weight=1)
        self.__root.after(REFRESH_RATE, lambda: self.__timer.count_down(lambda: self.__init_title_screen(end=True)))

    def __init_word(self, board: Board):
        """Displays the current word at the bottom of the window"""
        frame = Frame(self.__root, pady=PAD)
        frame.pack(side='bottom', fill='x')
        self.__word.pack(frame, board)
        Button(frame, text='Set', font=(FONT, FONTSIZE - 2), command=self.__check, sfx=False).grid(
            row=0, column=2, sticky='w'
        )

        for i in range(len(frame.children)):
            frame.columnconfigure(i, weight=1)

    # ---------------------------------------------------------------

    def __generate_board(self):
        """Creates a new board: clears the old one and loads a new board from randomizer"""
        self.__clear()
        frame = Frame(self.__root)
        frame.pack(side='right', fill='y', padx=(10, 0))
        self.__history.pack(frame)

        self.__init_score()
        self.__board = Frame(self.__root)
        self.__board.pack(fill='both', expand=True, padx=(PAD, 0))
        board = randomize_board()

        # Create a button for each letter
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                button = Button(self.__board, text=cell, font=("Courier", 25))
                button.bind('<Button>', self.__on_click, add='+')
                button.grid(row=i, column=j, padx=1, pady=1, sticky='nesw')
                self.__board.grid_columnconfigure(j, weight=1, uniform='button')
            self.__board.grid_rowconfigure(i, weight=1, uniform='1')
        self.__init_word(board)

    def __on_click(self, e: Event):
        """An onClick event which is resposible for toggling the button's state,
        and adding or removing the select letter from the current word"""
        path = self.__word
        button: Button = e.widget
        point = button.point()
        is_active = point in path.get()

        path.remove(point) if is_active else path.add(point)
        button.toggle(is_active, BLUE)

    def __check(self):
        """Checks if the current word in the dictionary, and gives the appropriate visual and auditorial response"""
        path = self.__word.get()
        word = is_valid_path(self.__word.board, path, self.__words)
        is_valid = word and word not in self.__history.get()
        color, sound = (GREEN, SUCCESS) if is_valid else (RED, FAIL)

        if is_valid:
            # Update the history and score
            self.__history.add(word)
            self.__score.add(len(path) ** 2)

        for button in self.__board.winfo_children():
            button: Button
            button.point() in path and button.flash(color)

        play(sound)
        self.__word.reset()

if __name__ == "__main__":
    Boggle(SIZE, SIZE).start()