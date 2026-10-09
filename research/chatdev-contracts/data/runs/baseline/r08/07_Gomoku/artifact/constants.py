'''
constants.py
Global configuration constants for the Gomoku game, including board
dimensions, rendering metrics, player/state identifiers, and colors
used by the graphical interface.
'''
# ---------------------------------------------------------------------------
# Board configuration
# ---------------------------------------------------------------------------
BOARD_SIZE = 15        # Standard Gomoku board: 15x15 intersections
WIN_COUNT = 5          # Consecutive stones required to win
# ---------------------------------------------------------------------------
# Player and cell values
# ---------------------------------------------------------------------------
EMPTY = 0              # Empty intersection
BLACK = 1              # Black stone (moves first)
WHITE = 2              # White stone
# ---------------------------------------------------------------------------
# Game states
# ---------------------------------------------------------------------------
STATE_ONGOING = "ongoing"
STATE_BLACK_WINS = "black_wins"
STATE_WHITE_WINS = "white_wins"
STATE_DRAW = "draw"
# ---------------------------------------------------------------------------
# Rendering metrics (pixels)
# ---------------------------------------------------------------------------
CELL_SIZE = 40         # Distance between adjacent intersections
MARGIN = 40            # Margin around the playing grid
STONE_RADIUS = 16      # Radius of a drawn stone
STAR_RADIUS = 4        # Radius of star-point (hoshi) markers
LINE_WIDTH = 1         # Grid line thickness
LAST_MOVE_MARKER_RADIUS = 3  # Radius of the last-move marker
CANVAS_SIZE = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)  # 640 px
# ---------------------------------------------------------------------------
# Colors (Tkinter color strings)
# ---------------------------------------------------------------------------
COLOR_BOARD = "#DCB35C"        # Wooden board background
COLOR_GRID = "#5A4621"         # Grid lines and star points
COLOR_STAR = "#5A4621"         # Star-point (hoshi) markers, same tone as grid lines
COLOR_BLACK_STONE = "#000000"  # Black stone fill
COLOR_WHITE_STONE = "#FFFFFF"  # White stone fill
COLOR_HIGHLIGHT = "#FF4500"    # Winning-stone highlight
COLOR_BG = "#F5F0E1"           # Window background
COLOR_TEXT = "#333333"         # Status text color
# ---------------------------------------------------------------------------
# Window configuration
# ---------------------------------------------------------------------------
WINDOW_TITLE = "Gomoku - Five in a Row"
STATUS_FONT = ("Arial", 14, "bold")
BUTTON_FONT = ("Arial", 12)