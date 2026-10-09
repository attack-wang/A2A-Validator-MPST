'''
Configuration constants for the Gomoku game.
Contains board geometry, player identifiers, colours and other
tuning values shared across all modules.
'''
# Board geometry
BOARD_SIZE = 15
CELL_SIZE = 40
MARGIN = 50
INFO_HEIGHT = 80
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN + INFO_HEIGHT
# Players / cell values
EMPTY = 0
BLACK = 1
WHITE = 2
PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}
# Rules
WIN_LENGTH = 5
# Visual settings
FPS = 60
STONE_RADIUS = CELL_SIZE // 2 - 4
STAR_POINTS = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
# Colours
COLOR_PAGE = (70, 50, 30)
COLOR_BACKGROUND = (222, 184, 135)
COLOR_GRID = (60, 40, 20)
COLOR_BLACK_STONE = (25, 25, 25)
COLOR_WHITE_STONE = (248, 248, 248)
COLOR_TEXT = (50, 30, 10)
COLOR_HIGHLIGHT = (200, 30, 30)
COLOR_PANEL = (245, 235, 215)
COLOR_BUTTON = (70, 130, 90)
COLOR_BUTTON_TEXT = (255, 255, 255)