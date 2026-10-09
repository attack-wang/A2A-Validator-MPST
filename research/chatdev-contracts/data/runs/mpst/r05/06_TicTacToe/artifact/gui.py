'''
gui.py
This module implements the graphical user interface for the tic-tac-toe
game using Tkinter (part of the Python standard library). It renders the
3x3 grid as clickable buttons, shows whose turn it is, announces the
winner or a draw, highlights the winning line, keeps a simple scoreboard
across rounds, and offers a "New Game" button to replay.
'''
import tkinter as tk
from tkinter import font as tkfont
from game_logic import TicTacToeGame
class TicTacToeGUI:
    """Tkinter front-end that drives a TicTacToeGame instance."""
    CELL_FONT_SIZE = 32
    HIGHLIGHT_COLOR = "#ffe08a"   # soft yellow for the winning line
    DEFAULT_CELL_COLOR = "#f0f0f0"
    def __init__(self, root, game=None):
        ...