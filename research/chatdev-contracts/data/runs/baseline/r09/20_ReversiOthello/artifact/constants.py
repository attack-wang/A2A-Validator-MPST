'''
constants.py
Shared constants for the Reversi (Othello) game: player colours, board size,
display colours and fonts.
'''
# Board / player values
EMPTY = 0
BLACK = 1
WHITE = 2
BOARD_SIZE = 8          # 8x8 grid
CELL_SIZE = 64          # pixel size of one cell
BOARD_PIXEL = BOARD_SIZE * CELL_SIZE
# Display colours (R, G, B)
BG_COLOR = (0, 128, 0)          # classic green felt
GRID_LINE_COLOR = (0, 60, 0)
BLACK_DISC_COLOR = (10, 10, 10)
WHITE_DISC_COLOR = (245, 245, 245)
HINT_COLOR = (60, 160, 60)
LAST_MOVE_COLOR = (255, 215, 0)  # gold ring for last placed disc
# Text / fonts
FONT_NAME = None                # use pygame default font
FONT_SIZE = 24
SCORE_FONT_SIZE = 28
MESSAGE_FONT_SIZE = 20
PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
# Window layout
INFO_PANEL_HEIGHT = 90
WINDOW_WIDTH = BOARD_PIXEL
WINDOW_HEIGHT = BOARD_PIXEL + INFO_PANEL_HEIGHT
# Animation
FLIP_FRAMES = 8         # number of frames for a disc flip animation
FLIP_DELAY_MS = 30      # delay between flip frames
FPS = 60
# GUI window caption
WINDOW_CAPTION = "Reversi (Othello)"