'''
ui.py
Tkinter UI: renders the 80x80 grid, info panel, and handles W/A/S/D input.
'''
import tkinter as tk
import config
from entities import Monster, TreasureChest
class GameUI:
    """Tkinter front-end for the Game: grid canvas + info panel."""
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.resizable(False, False)
        canvas_w = config.GRID_WIDTH * config.TILE_SIZE
        canvas_h = config.GRID_HEIGHT * config.TILE_SIZE
        self.canvas = tk.Canvas(self.root, width=canvas_w, height=canvas_h,
                                bg=config.COLOR_BACKGROUND,
                                highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=4, pady=4)
        self.info_panel = tk.Frame(self.root, width=config.INFO_PANEL_WIDTH,
                                   bg=config.COLOR_BACKGROUND)
        self.info_panel.grid(row=0, column=1, sticky="ns", padx=4, pady=4)
        self.info_panel.grid_propagate(False)
        self.hp_label = tk.Label(self.info_panel, text="", fg="white",
                                 bg=config.COLOR_BACKGROUND,
                                 font=("Helvetica", 12, "bold"),
                                 justify="left", anchor="nw")
        self.hp_label.pack(fill="x", pady=(8, 4))
        self.level_label = tk.Label(self.info_panel, text="", fg="white",
                                    bg=config.COLOR_BACKGROUND,
                                    font=("Helvetica", 11),
                                    justify="left", anchor="nw")
        self.level_label.pack(fill="x", pady=4)
        self.monster_label = tk.Label(self.info_panel, text="", fg="white",
                                      bg=config.COLOR_BACKGROUND,
                                      font=("Helvetica", 10),
                                      justify="left", anchor="nw")
        self.monster_label.pack(fill="x", pady=4)
        self.message_label = tk.Label(self.info_panel, text="", fg="#cccccc",
                                      bg=config.COLOR_BACKGROUND,
                                      font=("Helvetica", 9),
                                      justify="left", anchor="sw")
        self.message_label.pack(fill="both", expand=True, pady=4)
        self.root.bind("<Key>", self.on_key)
        self.rect_ids = [[None] * config.GRID_HEIGHT
                         for _ in range(config.GRID_WIDTH)]
        self.text_ids = [[None] * config.GRID_HEIGHT
                         for _ in range(config.GRID_WIDTH)]
        self.draw_full()
        self.update_info()