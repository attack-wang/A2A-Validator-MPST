'''
sudoku_gui.py
Tkinter-based graphical interface for the Sudoku game: grid rendering,
cell selection, keyboard/mouse input, mistake highlighting, and win detection.
'''
import tkinter as tk
from tkinter import messagebox, ttk
from sudoku_board import SudokuBoard
from sudoku_generator import SudokuGenerator
class SudokuGUI:
    """Main application window for the Sudoku puzzle game."""
    CELL_SIZE = 60
    GRID_PIXELS = CELL_SIZE * 9
    PADDING = 30
    BG_COLOR = "#faf8f1"
    GRID_LINE_COLOR = "#b0aca4"
    BOX_LINE_COLOR = "#4a4a4a"
    GIVEN_COLOR = "#2b2b2b"
    USER_COLOR = "#1565c0"
    ERROR_COLOR = "#d32f2f"
    SELECT_COLOR = "#bbdefb"
    PEER_COLOR = "#e8eaf6"  # highlight same row/col/box
    SAME_NUMBER_COLOR = "#c5cae9"
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)
        self.board = None
        self.solution = None
        self.selected = None  # (row, col) or None
        self.elapsed_seconds = 0
        self.timer_running = False
        self.game_over = False
        self.generator = SudokuGenerator()
        self._build_menu()
        self._build_canvas()
        self._build_controls()
        self._bind_keys()
        self.new_game("medium")
    ...