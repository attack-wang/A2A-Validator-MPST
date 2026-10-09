"""Main game class: tkinter window, game loop, states and collisions."""
import random
import tkinter as tk
import settings
import ui
from alien import ALIEN_PATTERN, AlienFleet, ALIEN_WIDTH, ALIEN_HEIGHT
from bullet import AlienBomb, PlayerBullet
from effects import Explosion
from ship import Ship
def _make_pixel_image(pattern, color, scale):
    """Render a text pattern into a tk.PhotoImage (one pixel block per 'X')."""
    width = len(pattern[0]) * scale
    height = len(pattern) * scale
    image = tk.PhotoImage(width=width, height=height)
    for r, row in enumerate(pattern):
        for c, ch in enumerate(row):
            if ch == "X":
                image.put(color, (c * scale, r * scale, (c + 1) * scale, (r + 1) * scale))
    return image
class Game:
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    STATE_VICTORY = "victory"
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(settings.WINDOW_TITLE)
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=settings.SCREEN_WIDTH,
                                height=settings.SCREEN_HEIGHT,
                                bg=settings.COLOR_BACKGROUND,
                                highlightthickness=0)
        self.canvas.pack()
        self.fonts = ui.load_fonts()
        self._load_images()
        self.high_score = 0
        self.keys = set()
        self._bind_keys()
        self.reset_game()
        self.state = self.STATE_MENU
        self._running = True
        self._last_time = None
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.after(settings.FRAME_MS, self._loop)
    def _load_images(self):
        self.alien_images = [
            _make_pixel_image(ALIEN_PATTERN, color, 3)
            for color in (settings.COLOR_PURPLE, settings.COLOR_ORANGE,
                          settings.COLOR_YELLOW, settings.COLOR_GREEN,
                          settings.COLOR_CYAN)
        ]
        ship_pattern = [
            "....X....",
            "....X....",
            "...XXX...",
            "..XXXXX..",
            ".XXXXXXX.",
            "XXXXXXXXX",
            "XXXXXXXXX",
        ]
        self.ship_image = _make_pixel_image(ship_pattern, settings.COLOR_CYAN, 5)
        self.ship_icon = self.ship_image  # small version for lives display
    ...