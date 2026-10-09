'''
gui.py
Tkinter graphical user interface for the Sudoku game.
This module consolidates the complete SudokuGUI class (previously
scattered across orphaned fragments) into one self-contained file.
It renders the 9x9 board on a Canvas, handles mouse/keyboard input,
highlights rule conflicts and wrong digits, provides Check/Hint/
Restart/New Game controls, a timer, and a completion dialog.
'''
import tkinter as tk
from tkinter import messagebox
from sudoku_board import SudokuBoard, GRID_SIZE, EMPTY
from puzzle_generator import PuzzleGenerator
# ------------------------------------------------------------------ layout
MARGIN = 20            # pixels between window edge and the board
CELL_SIZE = 48         # pixels per cell
BOARD_PIXELS = CELL_SIZE * GRID_SIZE
# ------------------------------------------------------------------ colors
BG_COLOR = "#f2f2f2"
BOARD_BG = "#ffffff"
SELECT_BG = "#bbdefb"
SAME_BG = "#e3f2fd"
CONFLICT_BG = "#ffcdd2"
LINE_THIN = "#b0b0b0"
LINE_BOLD = "#404040"
FIXED_TEXT = "#37474f"
USER_TEXT = "#1565c0"
MISTAKE_TEXT = "#ef6c00"
CONFLICT_TEXT = "#c62828"
STATUS_OK = "#2e7d32"
STATUS_ERR = "#c62828"
class SudokuGUI:
    """Main application window: board rendering, input handling and game flow."""
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku — ChatDev Edition")
        self.root.resizable(False, False)
        self.generator = PuzzleGenerator()
        self.board = None
        self.selected = None          # (row, col) or None
        self.game_over = False
        self.elapsed_seconds = 0
        self._timer_job = None
        self._build_menu()
        self._build_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<Key>", self.on_key_press)
        self.new_game("easy")
    ...