'''
Configuration constants for the Gomoku (Five in a Row) game.
This module centralizes every tunable value used across the project:
board dimensions, player codes, win conditions and GUI appearance.
'''
# ---------------------------------------------------------------------------
# Board and player settings
# ---------------------------------------------------------------------------
BOARD_SIZE = 15          # Standard Gomoku board: 15x15 intersections
EMPTY = 0                # Grid code for an empty intersection
BLACK = 1                # Grid code for a black stone (moves first)
WHITE = 2                # Grid code for a white stone
WIN_COUNT = 5            # Stones in an unbroken row needed to win
PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
# ---------------------------------------------------------------------------
# GUI geometry
# ---------------------------------------------------------------------------
CELL_SIZE = 40           # Pixel distance between two adjacent intersections
MARGIN = 40              # Pixel margin around the outermost intersections
STONE_RADIUS = 16        # Pixel radius of a drawn stone
BOARD_WIDTH = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)   # Canvas width  (640 px)
BOARD_HEIGHT = BOARD_WIDTH                                # Canvas height (square board)
# ---------------------------------------------------------------------------
# GUI colors (hex strings understood by tkinter)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = "#DCB35C"      # Wooden board background
COLOR_LINE = "#7A4A1E"            # Grid line color
COLOR_STAR = "#3B2412"            # Star point color
COLOR_BLACK_STONE = "#101010"     # Black stone fill
COLOR_WHITE_STONE = "#FAFAFA"     # White stone fill
COLOR_HIGHLIGHT = "#FF2222"       # Winning-line highlight
COLOR_STATUS_BG = "#F3E3C3"       # Status bar background
COLOR_STATUS_FG = "#333333"       # Status bar text color