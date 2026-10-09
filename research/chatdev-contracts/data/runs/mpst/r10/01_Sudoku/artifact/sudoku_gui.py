'''
sudoku_gui.py
Tkinter-based graphical interface for the classic Sudoku puzzle game.
'''
import tkinter as tk
from tkinter import messagebox, ttk
import time
from sudoku_engine import SudokuGenerator, SudokuBoard, EMPTY, DIGITS
CELL_FONT = ("Helvetica", 18, "bold")
CLUE_COLOR = "#2b3a55"  # dark blue for given clues
PLAYER_COLOR = "#1a6b3c"  # green for player entries? or dark
BG_NORMAL = "#ffffff"
BG_FIXED = "#e8eaf0"
BG_SELECTED = "#cfe8ff"
BG_CONFLICT = "#ffcccc"
BG_COMPLETE = "#d8f5d8"