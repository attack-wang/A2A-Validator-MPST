'''
game.py
Main application: window setup, the state machine (menu / playing /
game over / victory), the update loop, collision handling and drawing.
Built entirely on tkinter (Python standard library) so the game runs
without any third-party dependencies such as pygame.
'''
import random
import tkinter as tk
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien_fleet import AlienFleet
from explosion import Explosion
from scoreboard import Scoreboard
class Game:
    """Top-level game object that owns the loop and all entities."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(Settings.TITLE)
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root,
                                width=Settings.SCREEN_WIDTH,
                                height=Settings.SCREEN_HEIGHT,
                                bg=Settings.BG_COLOR,
                                highlightthickness=0)
        self.canvas.pack()
        self.root.configure(bg=Settings.BG_COLOR)
        self.keys = set()
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.fleet = None
        self.player_bullets = []
        self.alien_bullets = []
        self.explosions = []
        self.score = 0
        self.wave = 1
        self.state = "menu"  # menu, playing, game_over, victory
        self.wave_message_timer = 0.0
        self.running = True
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        self._schedule_loop()
        self.root.mainloop()
    def _schedule_loop(self):
        self.root.after(Settings.FRAME_MS, self._loop)
    def _loop(self):
        if not self.running:
            return
        dt = min(Settings.FRAME_MS / 1000.0, Settings.MAX_DT)
        try:
            self._update(dt)
            self._draw()
        finally:
            if self.running:
                self._schedule_loop()