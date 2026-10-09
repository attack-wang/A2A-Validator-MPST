'''
sudoku_gui.py
Tkinter front-end for the classic Sudoku game.
Features:
  * 9x9 clickable grid with bold separators between 3x3 subgrids
  * Mouse and keyboard input of digits 1-9 into empty cells
  * Live conflict highlighting (optional) and a "Check" button that
    reports wrong entries against the stored solution
  * Automatic completion detection with a congratulation dialog
  * New game (easy/medium/hard), hint, reveal solution, clear entries
  * Elapsed-time timer and status bar
'''
import random
import tkinter as tk
from tkinter import messagebox
from sudoku_logic import SudokuBoard
FONT = ('Helvetica', 18)
FONT_GIVEN = ('Helvetica', 18, 'bold')
FONT_USER = ('Helvetica', 18)
COLOR_BG = 'white'
COLOR_GIVEN_FG = 'black'
COLOR_USER_FG = '#1565c0'
COLOR_SELECTED = '#bbdefb'
COLOR_SAME = '#e3f2fd'
COLOR_MISTAKE_BG = '#ffcdd2'
COLOR_MISTAKE_FG = '#b71c1c'
COLOR_COMPLETE_BG = '#c8e6c9'
THICK = 3   # border width between 3x3 boxes
THIN = 1    # border width inside a box
class SudokuGUI:
    """Tkinter GUI that drives a SudokuBoard instance."""
    def __init__(self, root):
        self.root = root
        self.root.title('Sudoku')
        self.root.resizable(False, False)
        self.board = SudokuBoard()
        self.selected = None          # (row, col) or None
        self.mistake_cells = set()    # cells flagged by the Check button
        self.completed = False
        self.elapsed = 0
        self.timer_running = False
        self.difficulty_var = tk.StringVar(value='medium')
        self.live_conflicts = tk.BooleanVar(value=True)
        self.force_show_mistakes = False
        self.cells = [[None] * 9 for _ in range(9)]
        self._build_menu()
        self._build_grid()
        self._build_controls()
        self._build_status_bar()
        self._bind_keys()
        self.root.after(1000, self._tick)
        self.new_game('medium')
    ...