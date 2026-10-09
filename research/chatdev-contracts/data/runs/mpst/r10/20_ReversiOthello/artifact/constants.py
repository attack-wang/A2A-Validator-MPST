'''
constants.py
Global configuration constants for the Reversi (Othello) game.
Defines board dimensions, player identifiers, colours, and all
GUI-related sizing values used across the application.
'''
# ---------------------------------------------------------------------------
# Board / game constants
# ---------------------------------------------------------------------------
BOARD_SIZE = 8          # 8x8 grid
EMPTY = 0               # empty cell
BLACK = 1               # black player
WHITE = 2               # white player
PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
# All 8 directions (row_delta, col_delta)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
# ---------------------------------------------------------------------------
# GUI constants
# ---------------------------------------------------------------------------
FPS = 60
CELL_SIZE = 64                                   # pixel size of one cell
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE        # 512 px
SIDEBAR_WIDTH = 240
MARGIN = 20
WINDOW_WIDTH = BOARD_PIXEL_SIZE + SIDEBAR_WIDTH + MARGIN * 2
WINDOW_HEIGHT = BOARD_PIXEL_SIZE + MARGIN * 2
BOARD_X = MARGIN                 # top-left x of the board
BOARD_Y = MARGIN                 # top-left y of the board
SIDEBAR_X = BOARD_X + BOARD_PIXEL_SIZE + MARGIN
# Colours (R, G, B)
COLOR_BACKGROUND   = (30, 30, 30)
COLOR_BOARD        = (34, 120, 60)
COLOR_BOARD_ALT    = (28, 105, 52)
COLOR_GRID_LINE    = (18, 70, 35)
COLOR_TEXT         = (240, 240, 240)
COLOR_TEXT_DIM     = (170, 170, 170)
COLOR_HIGHLIGHT    = (255, 235, 120)
COLOR_VALID_DOT    = (255, 255, 255, 90)  # with alpha
COLOR_BUTTON       = (70, 70, 70)
COLOR_BUTTON_HOVER = (100, 100, 100)
COLOR_OVERLAY      = (0, 0, 0, 180)
COLOR_BLACK_DISC   = (15, 15, 15)
COLOR_WHITE_DISC   = (245, 245, 245)