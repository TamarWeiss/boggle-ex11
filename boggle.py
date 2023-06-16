from itertools import groupby
from tkinter import *
from tkinter import font

try: 
    from pygame import mixer
    SOUND_AVAILABLE = True 
except ImportError:
    SOUND_AVAILABLE = False

from boggle_board_randomizer import randomize_board
from ex11_utils import FILENAME, get_word, is_valid_path, load_words
from list_var import ListVar

#program constants: 
TIME = 180
REFRESH_RATE = 100
OG = 'SystemButtonFace'
FONT = 'sans serif'
FONTSIZE = 20
FULL_FONT = (FONT, FONTSIZE)
RED = '#ff8080'
GREEN = '#afef8f'
CLICK = 'click.mp3'
FAIL = 'honk.mp3'
SUCCESS = '1_up.wav'
HURRY = 'hurry-up.mp3'

class Boggle:
    ''' a class which manages a boggle game
    '''
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__score = IntVar(value=0)
        self.__words = load_words(FILENAME)
        self.__history = ListVar()
        self.__path = ListVar()
        self.__word = StringVar()
        self.__seconds = DoubleVar(value=TIME)
        self.__time = StringVar(value=self.format_time())
        if SOUND_AVAILABLE:
            mixer.init()
            self.__audio_player = mixer.music

        self.__path.trace_add('write', lambda *args: self.__word.set(get_word(self.get_board(), self.__path.get())))
        self.__seconds.trace_add('write', lambda *args: self.__time.set(self.format_time()))

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

    def __init_title_screen(self, end=False):
        """Initialize the title screen of the game. Also doubles as the end screen if end boolean is set to True"""
        self.__clear()
        self.__history.set([])

        #set content of button
        frame = Frame(self.__root)
        title = Label(frame, text='Boggle' if not end else 'Game Over!', font=(FONT, FONTSIZE + 10), pady=5)
        button = Button(frame, text='Play' if not end else 'Restart', font=FULL_FONT,
            command=self.__generate_board)

        frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        title.pack(side=TOP)
        #display final score
        if end:
            score = Label(frame, text=f'Final Score: {self.__score.get()}', font=FULL_FONT, pady=5)
            score.pack(side=TOP)
        button.pack(side=TOP, pady=10)

    def __init_history_sidebar(self):
        '''create a word history bar at the right side of the game window
        '''
        frame = Frame(self.__root)
        #create title and font
        f = font.Font(font=(FONT, FONTSIZE - 2))
        f.configure(underline=True)
        label = Label(frame, text='History', font=f)
        scrollbar = Scrollbar(frame, )
        #create the word history box with a scroll bar
        history = Listbox(frame,
            yscrollcommand=scrollbar.set,
            activestyle='none',
            bg=OG,
            selectbackground=OG,
            selectforeground='black',
            highlightthickness=0,
            font=(FONT, FONTSIZE - 6),
            listvariable=self.__history,
            width=10,
        )
        #the scroll bar controls the listbox
        scrollbar.config(command=history.yview)

        frame.pack(side='right', fill='y', padx=(10, 0))
        label.pack(pady=10)
        history.pack(side='left', fill='y', pady=(0, 10))
        scrollbar.pack(side='right', fill='y', pady=(0, 10))

    @staticmethod
    def init_var_label(root: Widget, text: str, var: Variable, i=0, fontsize=FONTSIZE - 2):
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
        self.__seconds.set(TIME)
        self.__score.set(0)

        #create and pack the frame.
        frame = Frame(self.__root)
        frame.pack(side='top', fill='x', padx=20, pady=10)
        #use the class method to create a static label with a 
        #dynamic label beneath it
        self.init_var_label(frame, 'Time:', self.__time, 0)
        self.init_var_label(frame, 'Score:', self.__score, 1)
        
        #ensure the two labels resize at a constant rate.
        for i in range(len(frame.children)):
            frame.columnconfigure(i, weight=1)
        #call the countdown method after 100 miliseconds
        self.__root.after(REFRESH_RATE, self.count_down)

    def format_time(self):
        '''get the remaining time in secods and format as minuets and seconds'''
        seconds = self.__seconds.get()
        return f'{int(seconds / 60)}:{str(round(seconds % 60, 2)).zfill(4)}'

    def count_down(self):
        """Counts down the timer. If it's done, it calls the end screen.
        plays a sound at 30 seconds. """
        #when does countdown start?
        seconds = round(self.__seconds.get(), 2)
        #checks if time remaining. if so decreases time by 100 miliseconds 
        #and calls itself again in 100 milliseconds
        if seconds > 0.1:
            self.__seconds.set(seconds - 0.1)
            if SOUND_AVAILABLE:
                seconds == 30 and self.play_sound(HURRY)
            self.__root.after(REFRESH_RATE, self.count_down)
        else:
            self.__init_title_screen(end=True)

    def __init_word_frame(self):
        ''' Create the widget for the current word'''
        self.__word.set('')
        frame = Frame(self.__root, pady=10)
        frame.pack(side='bottom', fill='x')

        #create the label and pack it
        self.init_var_label(frame, 'Word:', self.__word, 0)
        button = Button(frame, text='Set', font=(FONT, FONTSIZE - 2), command=self.check_word)
        button.grid(row=0, column=2, sticky=W)

        for i in range(3): frame.columnconfigure(i, weight=1)

    def __generate_board(self):
        '''creates a new board: clears the old one and loads a new board from randomizer
        '''
        self.__clear()
        self.__init_history_sidebar()
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
    def __button_coords(button: Widget):
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
        if SOUND_AVAILABLE: 
            self.play_sound(CLICK)

    @staticmethod
    def play_sound(filename: str):
        if not SOUND_AVAILABLE: return 
        mixer.music.load(filename)
        mixer.music.play(0)
    def check_word(self):
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
            self.__history.append(word)
            self.__score.set(self.__score.get() + len(path) ** 2)
        if SOUND_AVAILABLE: 
            self.play_sound(sound)
        self.flash_buttons(buttons, color)
        self.__path.set([])

    def flash_buttons(self, buttons: list[Widget], color=OG):
        '''chnages the color of all buttons in the current path'''
        for button in buttons:
            button: Button
            button.configure(bg=color)

        if color != OG:
            self.__board.after(250, self.flash_buttons, buttons)

    def get_board(self):
        '''return a 2d list of the board'''
        return [
            [button.cget('text') for button in row]
            for _, row in groupby(self.__board.winfo_children(), lambda button: self.__button_coords(button)[0])
        ]

    def start(self):
        self.__root.mainloop()

if __name__ == "__main__":
    size = 600
    Boggle(size, size).start()