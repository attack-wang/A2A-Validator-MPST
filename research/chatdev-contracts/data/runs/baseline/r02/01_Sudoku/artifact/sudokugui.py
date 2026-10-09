'''
sudoku_gui.py
Tkinter-based graphical user interface for the Sudoku game.
Responsibilities:
  * Render the 9x9 grid, given clues, and player entries on a Canvas.
  * Handle mouse clicks and keyboard input for cell selection and value entry.
  * Highlight rule conflicts in real time as the player types.
  * Provide "Check", "Reveal solution", and "New game" controls.
  * Detect completion and show a congratulation dialog.
'''
import time
import tkinter as tk
from tkinter import messagebox
from sudoku_board import SudokuBoard
class SudokuGUI:
    """Main application window: view + controller for the Sudoku game."""
    CELL_SIZE = 60
    MARGIN = 30
    WIDTH = MARGIN * 2 + CELL_SIZE * 9
    HEIGHT = MARGIN * 2 + CELL_SIZE * 9 + 0
    # --- colour palette -------------------------------------------------
    BG_COLOR = "#faf8f1"
    GRID_LINE = "#9e9e9e"
    GRID_LINE_BOLD = "#212121"
    SELECT_BG = "#bbdefb"
    PEER_BG = "#e3f2fd"
    SAME_BG = "#c8e6c9"
    CONFLICT_BG = "#ffcdd2"
    WRONG_BG = "#ffe0b2"
    GIVEN_FG = "#37474f"
    PLAYER_FG = "#1565c0"
    ERROR_FG = "#c62828"
    def __init__(self, root):
        self.root = root
        self.root.title("Classic Sudoku")
        self.root.resizable(False, False)
        # Game state
        self.board = SudokuBoard("Medium")
        self.selected = None
        self.solved = False
        self.start_time = time.time()
        self.elapsed = 0
        self._build_top_bar()
        self._build_canvas()
        self._build_bottom_bar()
        self._bind_events()
        self.redraw()
        self.root.after(200, self.update_timer)