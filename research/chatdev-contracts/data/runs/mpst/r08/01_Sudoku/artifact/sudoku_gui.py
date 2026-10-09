'''
sudoku_gui.py
Tkinter-based graphical interface for the Sudoku game: renders the 9x9
grid, handles cell selection and number input, highlights mistakes, and
detects completion.
'''
import random
import tkinter as tk
from tkinter import ttk, messagebox
from sudoku_board import SudokuBoard
from sudoku_generator import SudokuGenerator
CELL_SIZE = 60
GRID_SIZE = CELL_SIZE * 9
PAD = 20
class SudokuGUI:
    """Main application window for the Sudoku game."""
    GIVEN_COLOR = '#333333'
    PLAYER_COLOR = '#1565c0'
    MISTAKE_COLOR = '#d32f2f'
    SELECT_COLOR = '#bbdefb'
    PEER_COLOR = '#f5f5f5'
    HINT_COLOR = '#2e7d32'
    def __init__(self, root):
        self.root = root
        self.root.title('Sudoku')
        self.root.resizable(False, False)
        self.board = None
        self.selected = None  # (row, col) or None
        self.hinted = set()   # cells revealed by hints
        self._build_menu()
        self._build_controls()
        self._build_canvas()
        self._bind_keys()
        self.new_game('medium')
    ...