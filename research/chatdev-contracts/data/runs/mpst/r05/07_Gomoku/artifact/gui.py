'''
gui.py
Tkinter-based graphical interface for the Gomoku game.
This module renders the 15 x 15 board on a Tkinter Canvas, converts mouse
clicks to board intersections, draws stones / highlights, and drives the
GomokuGame controller. Every color, font and geometry value comes from
config.py — no magic numbers are hard-coded here.
'''
import tkinter as tk
from tkinter import messagebox
from config import (BOARD_SIZE, BLACK, WHITE, PLAYER_NAMES, PLAYER_SYMBOLS,
                    STAR_POINTS, CELL_SIZE, BOARD_PADDING, STONE_RADIUS,
                    HIGHLIGHT_RADIUS, CLICK_TOLERANCE, BG_COLOR, LINE_COLOR,
                    GRID_LINE_WIDTH, STAR_POINT_RADIUS, BLACK_COLOR,
                    WHITE_COLOR, WHITE_OUTLINE, HIGHLIGHT_COLOR,
                    STATUS_FONT, BUTTON_FONT)
from game import GomokuGame
class GomokuGUI:
    """Renders the Gomoku board and handles user interaction."""
    def __init__(self, master):
        self.master = master
        self.game = GomokuGame()
        self.stone_ids = {}  # (row, col) -> canvas item id
        master.title("Gomoku - Five in a Row")
        master.resizable(False, False)
        self.canvas_size = BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING
        self.status_bar = tk.Label(master, text="", font=STATUS_FONT, anchor="w")
        self.status_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.canvas = tk.Canvas(master, width=self.canvas_size,
                                height=self.canvas_size, bg=BG_COLOR,
                                highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.reset_button = tk.Button(self.button_frame, text="New Game",
                                      font=BUTTON_FONT, command=self.reset)
        self.reset_button.pack(side=tk.RIGHT)
        self.draw_board()
        self.update_status()
    # ------------------------------------------------------------------
    # Coordinate conversion
    # ------------------------------------------------------------------
    def coord_to_pixel(self, index):
        """Convert a board index (0..BOARD_SIZE-1) to a pixel coordinate."""
        return BOARD_PADDING + index * CELL_SIZE
    def pixel_to_coord(self, pixel):
        """Convert a pixel coordinate to the index of the nearest intersection.
        The value is rounded towards the intersection lying half a cell
        beyond the click, so the result may fall outside the board; callers
        must validate it with Board.is_valid_position().
        """
        return int((pixel - BOARD_PADDING + CELL_SIZE / 2) // CELL_SIZE)
    ...