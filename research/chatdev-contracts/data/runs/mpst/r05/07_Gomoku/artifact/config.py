'''
config.py
Global configuration constants for the Gomoku game application.
This module centralizes every tunable value used across the game:
board dimensions, player identifiers, GUI geometry, and colors.
Every constant defined here is consumed by board.py, game.py or gui.py,
so the GUI contains no hard-coded magic numbers or colors.
'''
# Board / game constants
BOARD_SIZE = 15
EMPTY = 0
BLACK = 1
WHITE = 2
PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
PLAYER_SYMBOLS = {BLACK: "●", WHITE: "○"}
WIN_LENGTH = 5
STAR_POINTS = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
# GUI constants
CELL_SIZE = 40
BOARD_PADDING = 40
STONE_RADIUS = 16
HIGHLIGHT_RADIUS = 4
CLICK_TOLERANCE = CELL_SIZE // 2
GRID_LINE_WIDTH = 2
STAR_POINT_RADIUS = 4
BG_COLOR = "#DCB35C"
LINE_COLOR = "#7A4A1E"
BLACK_COLOR = "#111111"
WHITE_COLOR = "#FFFFFF"
WHITE_OUTLINE = "#999999"
HIGHLIGHT_COLOR = "#FF3333"
STATUS_FONT = ("Arial", 13)
BUTTON_FONT = ("Arial", 11)