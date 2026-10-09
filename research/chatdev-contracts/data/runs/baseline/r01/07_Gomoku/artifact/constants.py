'''
constants.py
This module defines all global constants used across the Gomoku application,
including board dimensions, rendering metrics, player identifiers, colors,
and game state enumerations.
'''
from enum import Enum
# --- Board configuration ---
BOARD_SIZE = 15          # Standard Gomoku board: 15x15 intersections
WIN_COUNT = 5            # Number of aligned stones required to win
# --- Rendering configuration (pixels) ---
CELL_SIZE = 40           # Pixel distance between two adjacent intersections
MARGIN = 40              # Pixel padding around the board edges
STONE_RADIUS = 16        # Pixel radius of a stone
STATUS_BAR_HEIGHT = 60   # Pixel height of the bottom status frame (outside the canvas)
# Derived window dimensions
BOARD_PIXEL_SIZE = CELL_SIZE * (BOARD_SIZE - 1)          # 560
WINDOW_WIDTH = BOARD_PIXEL_SIZE + 2 * MARGIN             # 640
# The canvas only needs to contain the board plus its coordinate labels;
# the status bar lives in a separate frame packed below the canvas.
WINDOW_HEIGHT = BOARD_PIXEL_SIZE + 2 * MARGIN            # 640
# --- Colors ---
BOARD_COLOR = "#D9A45B"      # Wooden board background
GRID_LINE_COLOR = "#5A3A1A"  # Dark brown grid lines
STAR_POINT_COLOR = "#5A3A1A"
BLACK_STONE_COLOR = "#101010"
WHITE_STONE_COLOR = "#F5F5F5"
STONE_OUTLINE_COLOR = "#333333"
HIGHLIGHT_COLOR = "#E3333D"  # Winning line highlight
TEXT_COLOR = "#3A2A18"
LAST_MOVE_MARKER_COLOR = "#E3333D"
# --- Player identifiers ---
PLAYER_EMPTY = 0
PLAYER_BLACK = 1
PLAYER_WHITE = 2
class GameState(Enum):
    """Enumeration of all possible states of a Gomoku game."""
    ONGOING = "ongoing"
    BLACK_WIN = "black_win"
    WHITE_WIN = "white_win"
    DRAW = "draw"