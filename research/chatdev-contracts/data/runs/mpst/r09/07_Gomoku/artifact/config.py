'''
config.py
Central configuration constants for the Gomoku game:
board geometry, window layout, colors, fonts and messages.
'''
# --- Board geometry -------------------------------------------------------
BOARD_SIZE = 15                       # Standard Gomoku: 15x15 intersections
CELL_SIZE = 42                        # Pixels between adjacent intersections
MARGIN = 50                           # Padding around the playing grid
# --- Window layout --------------------------------------------------------
BOARD_PIXEL_SIZE = CELL_SIZE * (BOARD_SIZE - 1)          # Grid span in pixels
WINDOW_WIDTH = MARGIN * 2 + BOARD_PIXEL_SIZE             # 50*2 + 42*14 = 688
STATUS_BAR_HEIGHT = 70
WINDOW_HEIGHT = MARGIN * 2 + BOARD_PIXEL_SIZE + STATUS_BAR_HEIGHT
FPS = 60
# --- Players --------------------------------------------------------------
EMPTY = 0
PLAYER_BLACK = 1
PLAYER_WHITE = 2
# --- Stone rendering ------------------------------------------------------
STONE_RADIUS = CELL_SIZE // 2 - 4
LAST_MOVE_MARKER_COLOR = (220, 40, 40)
# --- Colors (R, G, B) -----------------------------------------------------
COLOR_BACKGROUND = (222, 184, 135)    # Wooden board tone
COLOR_LINE = (70, 45, 20)             # Dark brown grid lines
COLOR_STAR = (70, 45, 20)             # Star point markers
COLOR_BLACK_STONE = (25, 25, 25)
COLOR_WHITE_STONE = (250, 250, 250)
COLOR_TEXT = (45, 28, 12)
COLOR_WIN_HIGHLIGHT = (210, 40, 40)
COLOR_PANEL = (245, 235, 215)
COLOR_BUTTON = (70, 130, 90)
COLOR_BUTTON_HOVER = (95, 165, 115)
# --- Fonts ----------------------------------------------------------------
FONT_SIZE_STATUS = 26
FONT_SIZE_BUTTON = 22
# --- Status messages ------------------------------------------------------
MSG_BLACK_TURN = "Black player's turn - click an intersection to place a stone"
MSG_WHITE_TURN = "White player's turn - click an intersection to place a stone"
MSG_BLACK_WIN = "Black wins with five in a row! Press Restart or R to play again."
MSG_WHITE_WIN = "White wins with five in a row! Press Restart or R to play again."
MSG_DRAW = "The board is full - it's a draw! Press Restart or R to play again."