'''
constants.py
This module defines all global constants used throughout the Reversi (Othello)
game, including board dimensions, player representations, colors, directions,
and UI layout parameters.
'''
# Board configuration
BOARD_SIZE = 8          # Standard 8x8 Reversi grid
CELL_SIZE = 80          # Pixel size of each grid cell
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE  # 640 pixels
# Score panel configuration
PANEL_HEIGHT = 100      # Height of the score/status panel below the board
WINDOW_WIDTH = BOARD_PIXEL_SIZE
WINDOW_HEIGHT = BOARD_PIXEL_SIZE + PANEL_HEIGHT
FPS = 30
# Player representations
EMPTY = 0
BLACK = 1
WHITE = 2
PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
# The eight directions used to search for flippable discs
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
# Colors (R, G, B)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_BOARD = (0, 128, 0)        # Classic green board
COLOR_GRID_LINE = (0, 90, 0)
COLOR_BLACK_DISC = (10, 10, 10)
COLOR_WHITE_DISC = (245, 245, 245)
COLOR_VALID_MOVE = (144, 238, 144)  # Light green hint
COLOR_TEXT = (255, 255, 255)
COLOR_PANEL = (50, 50, 50)
COLOR_OVERLAY = (0, 0, 0, 180)   # Semi-transparent overlay (RGBA)
COLOR_HIGHLIGHT = (255, 215, 0)  # Gold for last move highlight
# Window caption
WINDOW_CAPTION = "Reversi (Othello)"