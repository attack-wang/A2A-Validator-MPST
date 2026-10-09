'''
Constants and configuration for the Reversi (Othello) game.
'''
# Board dimensions
BOARD_SIZE = 8  # 8x8 grid
CELL_SIZE = 70  # pixels per cell
INFO_HEIGHT = 100  # height of the info/score panel
# Window dimensions
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + INFO_HEIGHT
# Player representations
EMPTY = 0
BLACK = 1
WHITE = 2
# Player names
PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
# Colors (R, G, B)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_BOARD_GREEN = (0, 128, 0)
COLOR_GRID_LINE = (0, 0, 0)
COLOR_BLACK_DISC = (10, 10, 10)
COLOR_WHITE_DISC = (245, 245, 245)
COLOR_VALID_MOVE = (144, 238, 144)
COLOR_TEXT = (255, 255, 255)
COLOR_INFO_PANEL = (50, 50, 50)
COLOR_LAST_MOVE = (255, 215, 0)  # gold highlight for last move
# Game title
GAME_TITLE = "Reversi (Othello)"