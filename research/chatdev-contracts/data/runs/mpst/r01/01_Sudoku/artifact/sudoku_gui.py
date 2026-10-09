'''
sudoku_gui.py
Graphical user interface for the Sudoku game, built with tkinter.
This module contains the SudokuGUI class, which provides:
- A 9x9 interactive grid of cells
- Cell selection via mouse clicks
- Digit entry via keyboard (1-9), deletion via Backspace/Delete/0
- Real-time mistake highlighting (conflicting cells shown in red)
- Completion detection with a congratulatory message
- New game / restart controls with difficulty selection
- A hint feature that reveals the correct value for the selected cell
'''
import tkinter as tk
from tkinter import messagebox, ttk
from sudoku_board import SudokuBoard
class SudokuGUI:
    """Tkinter-based GUI for the classic Sudoku puzzle game."""
    CELL_SIZE = 3  # font size scaling helper
    def __init__(self, master):
        self.master = master
        self.master.title("Classic Sudoku")
        self.master.resizable(False, False)
        self.board = SudokuBoard()
        self.selected = None  # (row, col) of currently selected cell
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self._build_menu()
        self._build_grid()
        self._build_controls()
        self._bind_keys()
        self.new_game("medium")
    ...