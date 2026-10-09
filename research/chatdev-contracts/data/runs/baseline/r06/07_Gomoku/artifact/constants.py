'''
constants.py
Global configuration and shared constants for the Gomoku game,
including board dimensions, window size, colors, player identifiers,
and status messages.
'''
# ---------------------------------------------------------------------------
# Board configuration
# ---------------------------------------------------------------------------
BOARD_SIZE = 15      # Standard Gomoku board: 15x15 intersections
CELL_SIZE = 40       # Pixel distance between two adjacent intersections
MARGIN = 50          # Pixel margin around the board (space for coordinates)
STONE_RADIUS = 16    # Pixel radius of a stone
# Total pixel size of the square board area
BOARD_PIXEL_SIZE = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)
# ---------------------------------------------------------------------------
# Window configuration
# ---------------------------------------------------------------------------
STATUS_BAR_HEIGHT = 50
WINDOW_WIDTH = BOARD_PIXEL_SIZE
WINDOW_HEIGHT = BOARD_PIXEL_SIZE + STATUS_BAR_HEIGHT
WINDOW_TITLE = "Gomoku - Five in a Row"
FPS = 60
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (222, 184, 135)    # Wooden board color
COLOR_LINE = (70, 45, 20)             # Dark brown grid lines
COLOR_STATUS_BG = (245, 240, 225)     # Status bar background
COLOR_TEXT = (30, 30, 30)             # Status text color
COLOR_BLACK = (20, 20, 20)            # Black stone
COLOR_WHITE = (250, 250, 250)         # White stone
COLOR_WHITE_OUTLINE = (110, 110, 110) # Outline so white stones stay visible
COLOR_LAST_MOVE = (220, 40, 40)       # Red ring marking the last move
COLOR_WIN = (255, 120, 0)             # Orange ring marking the winning line
# ---------------------------------------------------------------------------
# Player identifiers (board cell values)
# ---------------------------------------------------------------------------
EMPTY = 0
BLACK = 1
WHITE = 2
# ---------------------------------------------------------------------------
# Status messages
# ---------------------------------------------------------------------------
MSG_BLACK_TURN = "Black's turn - click an intersection to place a stone"
MSG_WHITE_TURN = "White's turn - click an intersection to place a stone"
MSG_BLACK_WIN = "Black wins with five in a row!"
MSG_WHITE_WIN = "White wins with five in a row!"
MSG_DRAW = "The board is full - it's a draw!"
MSG_RESTART_HINT = "Press R to start a new game"