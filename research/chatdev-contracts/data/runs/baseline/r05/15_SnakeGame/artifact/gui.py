'''
gui.py
Tkinter front end for the Snake game: window management, the main
event/render loop, the difficulty-selection menu, the in-game HUD, and
the pause / game-over overlays. Uses only the standard library.
'''
import sys
import time
import tkinter as tk
import config
from game import Game
class GameGUI:
    '''
    Owns the tkinter window and the application state machine
    (MENU -> PLAYING <-> PAUSED -> GAME_OVER) and drives rendering.
    '''
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.resizable(False, False)
        self.root.configure(bg=config.COLOR_BACKGROUND)
        self.canvas = tk.Canvas(
            self.root,
            width=config.WINDOW_WIDTH,
            height=config.WINDOW_HEIGHT,
            bg=config.COLOR_BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()
        self._load_fonts()
        self.state = config.STATE_MENU
        self.menu_index = 1  # default selection: Medium
        self.game = None
        self._tick_accumulator = 0.0
        self._last_time = time.monotonic()
        self.root.bind("<Key>", self._handle_keydown)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._schedule_loop()
    # ------------------------------------------------------------------
    # Setup helpers
    # ------------------------------------------------------------------
    def _load_fonts(self):
        '''Create the font tuples used on the various screens.'''
        self.font_small = ("Consolas", 12)
        self.font_medium = ("Consolas", 14, "bold")
        self.font_large = ("Consolas", 30, "bold")
    ...