'''
constants.py
Configuration constants for the Tic-Tac-Toe game, including window
dimensions, grid geometry, colors, and font settings.
'''
# --- Window -----------------------------------------------------------
WINDOW_WIDTH = 480          # Window width in pixels
WINDOW_HEIGHT = 650         # Window height in pixels
WINDOW_TITLE = "Tic-Tac-Toe"
FPS = 60                    # Frames per second
# --- Grid geometry ----------------------------------------------------
GRID_SIZE = 3               # Standard 3x3 board
CELL_SIZE = 140             # Size of one cell in pixels
BOARD_PIXEL_SIZE = CELL_SIZE * GRID_SIZE          # 420 px
GRID_LEFT = (WINDOW_WIDTH - BOARD_PIXEL_SIZE) // 2  # Centered horizontally
GRID_TOP = 110              # Top edge of the board (below the status text)
# --- Restart button ---------------------------------------------------
BUTTON_WIDTH = 190
BUTTON_HEIGHT = 50
BUTTON_MARGIN_TOP = 35      # Space between board bottom and button
# --- Colors (R, G, B) -------------------------------------------------
COLOR_BACKGROUND = (28, 32, 48)      # Dark navy background
COLOR_GRID = (200, 205, 220)         # Light gray grid lines
COLOR_TEXT = (235, 240, 250)         # Near-white text
COLOR_X = (86, 156, 214)             # Blue for player X
COLOR_O = (231, 106, 95)             # Red for player O
COLOR_HOVER = (58, 64, 92)           # Highlight for hovered empty cell
COLOR_WIN_CELL = (52, 96, 66)        # Green tint for winning cells
COLOR_BUTTON = (70, 78, 110)         # Restart button fill
COLOR_BUTTON_HOVER = (98, 108, 150)  # Restart button fill on hover
COLOR_HINT = (150, 158, 180)         # Muted color for the bottom hint bar
# --- Fonts ------------------------------------------------------------
FONT_NAME = "arial"
FONT_SIZE_STATUS = 30
FONT_SIZE_MARK = 96
FONT_SIZE_BUTTON = 24
FONT_SIZE_HINT = 16