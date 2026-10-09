'''
gui.py
This module provides the Tkinter-based graphical front-end of the Gomoku game.
GomokuGUI renders the 15x15 wooden board, draws black/white stones, converts
mouse clicks into board intersections, displays game status messages, marks
the last played stone, highlights the winning line and offers a restart
button. All game rules are delegated to the GameController.
'''
import tkinter as tk
from constants import (BOARD_SIZE, CELL_SIZE, MARGIN, STONE_RADIUS,
                       BOARD_PIXEL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT,
                       BOARD_COLOR, GRID_LINE_COLOR, STAR_POINT_COLOR,
                       STONE_OUTLINE_COLOR, HIGHLIGHT_COLOR, TEXT_COLOR,
                       LAST_MOVE_MARKER_COLOR, GameState)
from game_controller import GameController
# The five standard star (hoshi) points of a 15x15 Gomoku board.
STAR_POINTS = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
COLUMN_LABELS = "ABCDEFGHJKLMNOP"  # hmm, Gomoku usually uses A-O including I? 