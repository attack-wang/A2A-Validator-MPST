'''
gui.py
Tkinter graphical user interface for the Minesweeper game.
...
'''
import tkinter as tk
from tkinter import messagebox
from game_logic import Board, Difficulty
# Classic Minesweeper colour scheme for the number hints.
NUMBER_COLORS = {
    1: "#0000FF",  # blue
    2: "#008000",  # green
    3: "#FF0000",  # red
    4: "#000080",  # navy
    5: "#800000",  # maroon
    6: "#008080",  # teal
    7: "#000000",  # black
    8: "#808080",  # gray
}
FLAG_SYMBOL = "\u2691"   # ⚑
MINE_SYMBOL = "\u25CF"   # ●
WRONG_FLAG_SYMBOL = "\u2715"  # ✕ overlay -> I'll render "✕●"? maybe "●" with X... simpler: "✗"