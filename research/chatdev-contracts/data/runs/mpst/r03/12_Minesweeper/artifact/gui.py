'''
gui.py
Tkinter front-end for the Minesweeper game.
Renders the minefield on a Canvas, provides the classic header panel
(mine counter, reset button, timer), a menu bar with difficulty
selection, and full mouse interaction:
    left click  - uncover a cell
    right click - toggle a flag on a covered cell
    middle click- chord on a revealed number
The board is redrawn after every single move.
'''
import tkinter as tk
from tkinter import messagebox
from board import Board, CellState
from config import (DIFFICULTIES, DEFAULT_DIFFICULTY, CELL_SIZE,
                    BORDER_WIDTH, COLORS, NUMBER_COLORS,
                    FONT_COUNTER, FONT_FACE, FONT_STATUS, FONT_ABOUT,
                    FONT_NUMBER, FONT_LED, MAX_TIME)
class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.difficulty_name = DEFAULT_DIFFICULTY
        self.board = None
        self.time = 0
        self._timer_id = None
        self._game_finished = False  # dialog already shown for this game
        self._build_menu()
        self._build_widgets()
        self.new_game(DEFAULT_DIFFICULTY)
    ...