import tkinter

from components.music import play
from consts import Point, OG

CLICK = 'click.mp3'
DURATION = 250

class Button(tkinter.Button):
    """An extended Button class, which adds support for click sfxs, and toggling or flashing in a chosen color"""

    def __init__(self, *args, sfx=True, **kwargs):
        super().__init__(*args, **kwargs)
        sfx and self.bind("<Button>", lambda *args: play(CLICK), add="+")

    def point(self) -> Point:
        """Returns the button's placement on the board (if it has any)"""
        grid_info = self.grid_info()
        return (grid_info.get('row', 0), grid_info.get('column', 0))

    def toggle(self, is_active: bool, color: str):
        """Switched between an active color and a default color based on its active state"""
        self.configure(bg=color if not is_active else OG)

    def flash(self, color=OG, duration=DURATION):
        """Flashes the button in a certain color for a given duration"""
        self.configure(bg=color)
        if color != OG:
            self.after(duration, self.flash)