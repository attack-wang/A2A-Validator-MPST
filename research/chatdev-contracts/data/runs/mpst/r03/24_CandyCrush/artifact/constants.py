"""
constants.py
Central configuration for the Candy Match-3 game.
Contains all tunable parameters: screen/board dimensions, colors,
candy definitions, animation speeds, scoring rules and game balance
values. Keeping them in one place makes the game easy to tweak.
"""
# ---------------------------------------------------------------------------
# Screen / layout
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 800
FPS = 60
GRID_ROWS = 8
GRID_COLS = 8
CELL_SIZE = 64
BOARD_WIDTH = GRID_COLS * CELL_SIZE
BOARD_HEIGHT = GRID_ROWS * CELL_SIZE
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 210
# ---------------------------------------------------------------------------
# Colors
# ...