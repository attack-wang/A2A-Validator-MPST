'''
sudoku_gui.py
Tkinter front-end for the classic Sudoku puzzle game.
Renders the 9x9 grid, handles keyboard/mouse input, highlights rule
conflicts in real time, offers New Game / difficulty / Check / Clear /
Hint controls, and celebrates when the puzzle is completed correctly.
'''
import tkinter as tk
from tkinter import ttk, messagebox
from sudoku_engine import SudokuBoard
from puzzle_generator import PuzzleGenerator
class SudokuGUI(tk.Tk):
    """Main application window for the Sudoku game."""
    GRID_BG = "#2b2b2b"       # colour of the thick subgrid separators
    GIVEN_FG = "#ffffff"      # pre-filled digits
    USER_FG = "#4fc3f7"       # digits typed by the player
    ERROR_BG = "#8b3a3a"      # highlight for conflicting cells
    SELECTED_BG = "#39566b"   # highlight for the focused cell
    SOLVED_BG = "#2e7d32"     # celebration green
    DEFAULT_BG = "#1e1e1e"    # normal cell background
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.resizable(False, False)
        self.generator = PuzzleGenerator()
        self.board = SudokuBoard()
        self.solution = None
        self.solved = False
        self.entries = [[None] * 9 for _ in range(9)]
        self._widget_map = {}
        self._build_menu()
        self._build_grid()
        self._build_status_bar()
        self.new_game(difficulty=PuzzleGenerator.EASY)
    ...