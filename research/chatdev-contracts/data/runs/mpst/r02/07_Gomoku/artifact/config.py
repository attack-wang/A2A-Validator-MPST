'''
config.py
Central configuration constants for the Gomoku application.
Includes board dimensions, player identifiers, pixel layout
values, visual styling colors, and fonts used across the GUI.
This module contains constants only - no logic, no GUI code.
'''
# Board and gameplay constants
BOARD_SIZE = 15            # Standard Gomoku board: 15x15 intersections
EMPTY = 0                  # Cell state: no stone
PLAYER_BLACK = 1           # Cell state / player id: black (moves first)
PLAYER_WHITE = 2           # Cell state / player id: white
# Layout constants (pixels)
CELL_SIZE = 40             # Pixel distance between adjacent intersections
MARGIN = 30                # Pixel border around the grid
STONE_RADIUS = 18          # Pixel radius of a stone
BOARD_PIXELS = CELL_SIZE * (BOARD_SIZE - 1) + 2 * MARGIN  # Canvas size
# Visual styling
BOARD_COLOR = "#DCB35C"
GRID_LINE_COLOR = "#000000"
BLACK_STONE_COLOR = "#000000"
WHITE_STONE_COLOR = "#FFFFFF"
HIGHLIGHT_COLOR = "#FF0000"
STATUS_BG_COLOR = "#F0F0F0"
TEXT_COLOR = "#000000"
# Window text and fonts
WINDOW_TITLE = "Gomoku - Five in a Row"
STATUS_FONT = ("Arial", 14)
BUTTON_FONT = ("Arial", 12)