'''
Global configuration constants for the Candy Crush-style match-3 game.
'''
# Screen / board layout
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 760  # board + HUD space
GRID_SIZE = 8
CELL_SIZE = 64
BOARD_WIDTH = GRID_SIZE * CELL_SIZE  # 512
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE
BOARD_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2  # 64
BOARD_Y = 180  # leave room for HUD on top
# FPS
FPS = 60
# Candy types
NUM_CANDY_TYPES = 6
# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
...