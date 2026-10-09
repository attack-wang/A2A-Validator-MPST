'''
ui.py
Minimal tkinter user interface: renders the 80x80 grid, handles
W/A/S/D input and shows the player's HP plus encountered monster stats.
'''
import tkinter as tk
import config
from game import Game
class GameUI:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.root.title("Tower of the Sorcerer - Roguelike")
        self.root.resizable(False, False)
        self._build_layout()
        self._bind_keys()
        self._tile_ids = None
        self._player_id = None
        self.render_full()
        self.update_panel()
    def _build_layout(self):
        main frame; canvas; side panel with:
          - Level label
          - HP label (big)
          - HP bar? minimal: label. Maybe a simple canvas bar. Keep label + optional bar. I'll add a small HP bar for clarity — still minimal.
          - "Nearby monsters" list (Text widget small)
          - "Last combat" label
          - message log (Text widget, disabled)
          - Restart button
          - legend