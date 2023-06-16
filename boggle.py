from itertools import groupby
from tkinter import *

from boggle_board_randomizer import randomize_board
from components.history import History
from components.list_var import ListVar
from components.music import Music
from components.score import Score
from components.timer import Timer
from consts import *
from ex11_utils import FILENAME, get_word, is_valid_path, load_words

class Boggle:
    ''' a class which manages a boggle game
    '''
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__words = load_words(FILENAME)
        self.__path = ListVar()
        self.__word = StringVar()

        self.__history = History()
        self.__music = Music()
        self.__timer = Timer(TIME)
        self.__score = Score()

        self.__root.title('Boggle')
        self.__path.trace_add('write', lambda *args: self.__word.set(get_word(self.get_board(), self.__path.get())))
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
        self.__root.mainloop()

    # ---------------------------------------------------

    def __init_title_screen(self, end=False):
        """Initialize the title screen of the game. Also doubles as the end screen if end boolean is set to True"""
        self.__clear()
        self.__history.reset()

        #set content of button
        frame = Frame(self.__root)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(frame, text='Boggle' if not end else 'Game Over!', font=(FONT, FONTSIZE + 10), pady=5).pack(side='top')
        end and self.__score.pack_result(frame)
        Button(
            frame, text='Play' if not end else 'Restart', font=FULL_FONT, command=self.__generate_board
        ).pack(side='top', pady=PAD)

    @staticmethod
    def __init_var_label(root: Widget, text: str, var: Variable, i=0, fontsize=FONTSIZE - 2):
        ''' a class method for making a pair of labels in a widget: 'text' 
        is a static label above var, which is a dynamically changing label
        '''
        #the static label
        label = Label(root, text=text, font=(FONT, fontsize))
        #the dynamic label
        var_label = Label(root, textvariable=var, font=(FONT, fontsize))
        
        #add the labels to the widget
        label.grid(row=0, column=2 * i, sticky=E)
        var_label.grid(row=0, column=2 * i + 1, padx=5, sticky=W)

    def __init_score_frame(self):
        ''' display score and time at the top of the window
        '''
        #initialise time to number of seconds for a game
        self.__score.reset()
        self.__timer.reset()

        #create and pack the frame.
        frame = Frame(self.__root)
        frame.pack(side='top', fill='x', padx=2 * PAD, pady=PAD)
        #use the class method to create a static label with a 
        #dynamic label beneath it
        self.__score.pack(frame)
        self.__timer.pack(frame)
        
        #ensure the two labels resize at a constant rate.
        for i in range(len(frame.children)):
            frame.columnconfigure(i, weight=1)
        self.__root.after(REFRESH_RATE, lambda: self.__timer.count_down(lambda: self.__init_title_screen(end=True)))

    def __init_word_frame(self):
        ''' Create the widget for the current word'''
        self.__word.set('')
        frame = Frame(self.__root, pady=PAD)
        frame.pack(side='bottom', fill='x')

        #create the label and pack it
        self.__init_var_label(frame, 'Word:', self.__word, 0)
        Button(frame, text='Set', font=(FONT, FONTSIZE - 2), command=self.check).grid(row=0, column=2, sticky='w')
        for i in range(len(frame.children)):
            frame.columnconfigure(i, weight=1)

    # ---------------------------------------------------------------

    def __generate_board(self):
        '''creates a new board: clears the old one and loads a new board from randomizer
        '''
        self.__clear()

        frame = Frame(self.__root)
        frame.pack(side='right', fill='y', padx=(10, 0))
        self.__history.pack(frame)
        self.__init_score_frame()

        self.__board = Frame(self.__root)
        self.__board.pack(fill='both', expand=True, padx=(10, 0))
        board = randomize_board()

        #create a button for each location
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                button = Button(self.__board, text=cell, font=("Courier", 25))
                #bind an even handler to the buttons which triggers when clicked
                button.bind('<Button-1>', self.__on_click)
                button.grid(row=i, column=j, padx=1, pady=1, sticky='nesw')
                self.__board.grid_columnconfigure(j, weight=1, uniform='button')
            self.__board.grid_rowconfigure(i, weight=1, uniform='1')

        self.__init_word_frame()

    @staticmethod
    def __button_coords(button: Widget) -> Point:
        ''' a helper function for processing what happens when I press a button'''
        grid_info = button.grid_info()
        return (grid_info['row'], grid_info['column'])

    def __on_click(self, e: Event):
        '''handle click: change color of a cell on the board and update the path'''
        path = self.__path
        button: Button = e.widget
        point = self.__button_coords(button)
        is_active = point in path.get()

        #change button color and update path
        button.configure(bg='#b5d4e3' if not is_active else OG)
        path.remove(point) if is_active else path.append(point)
        self.__music.play(CLICK)

    def check(self):
        ''' check if the current word in the dictionary'''
        path = self.__path.get()
        word = is_valid_path(self.get_board(), path, self.__words)
        is_valid = word and word not in self.__history.get()
        color, sound = (GREEN, SUCCESS) if is_valid else (RED, FAIL)
        buttons = [
            button for button in self.__board.winfo_children()
            if self.__button_coords(button) in self.__path
        ]

        if is_valid:
            #update the history and score
            self.__history.add(word)
            self.__score.add(len(path) ** 2)
            self.__music.play(sound)
        self.flash_buttons(buttons, color)
        self.__path.set([])

    def flash_buttons(self, buttons: list[Widget], color=OG):
        '''chnages the color of all buttons in the current path'''
        for button in buttons:
            button: Button
            button.configure(bg=color)

        if color != OG:
            self.__board.after(250, self.flash_buttons, buttons)

    def get_board(self) -> Board:
        '''return a 2d list of the board'''
        return [
            [button.cget('text') for button in row]
            for _, row in groupby(self.__board.winfo_children(), lambda button: self.__button_coords(button)[0])
        ]

if __name__ == "__main__":
    Boggle(SIZE, SIZE).start()