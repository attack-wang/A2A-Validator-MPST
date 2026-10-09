'''
minesweeper_gui.py
Tkinter graphical front-end for the Minesweeper game.
Contains:
- DIFFICULTIES: preset board configurations (beginner / intermediate / expert).
- MinesweeperGUI: builds the window, renders the board as a grid of buttons,
  handles mouse input (left click = reveal, right click = flag,
  middle click = chord), keeps the timer and mine counter up to date and
  shows the end-of-game state.
'''
import tkinter as tk
from tkinter import messagebox, Menu
from game_board import Board
DIFFICULTIES = {
    "Beginner": {"rows": 9, "cols": 9, "mines": 10},
    "Intermediate": {"rows": 16, "cols": 16, "mines": 40},
    "Expert": {"rows": 16, "cols": 30, "mines": 99},
}
CELL_SIZE = 28  # pixels per cell
# Classic Minesweeper colours for the number hints.
NUMBER_COLORS = {
    1: "#0000FF",
    2: "#008000",
    3: "#FF0000",
    4: "#000080",
    5: "#800000",
    6: "#008080",
    7: "#000000",
    8: "#808080",
}
FLAG_SYMBOL = "🚩"
MINE_SYMBOL = "💥"