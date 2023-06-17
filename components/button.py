import tkinter

from components.music import play
from consts import Point, OG

CLICK = 'click.mp3'
DURATION = 250

class Button(tkinter.Button):
    def __init__(self, *args, sfx=True, **kwargs):
        super().__init__(*args, **kwargs)
        sfx and self.bind("<Button>", lambda *args: play(CLICK), add="+")

    def point(self) -> Point:
        grid_info = self.grid_info()
        return (grid_info.get('row', 0), grid_info.get('column', 0))

    def toggle(self, is_active: bool, color: str):
        self.configure(bg=color if not is_active else OG)

    def flash(self, color=OG):
        self.configure(bg=color)
        if color != OG:
            self.after(DURATION, self.flash)