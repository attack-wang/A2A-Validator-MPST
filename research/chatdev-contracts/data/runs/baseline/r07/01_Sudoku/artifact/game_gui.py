'''
game_gui.py
Tkinter-based graphical interface for the Sudoku game.
'''
import time
import tkinter as tk
from tkinter import messagebox
from sudoku_board import SudokuBoard
from sudoku_generator import SudokuGenerator
CELL_SIZE = 52
GRID_SIZE = CELL_SIZE * 9
BG_FIXED = ...