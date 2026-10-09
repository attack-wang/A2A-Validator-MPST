'''
constants.py
Central configuration constants for the Gomoku game.
'''
# --- Board configuration ---
BOARD_SIZE = 15          # Standard Gomoku board: 15x15 intersections
EMPTY = 0                # Value representing an empty intersection
BLACK = 1                # Value representing a black stone
WHITE = 2                # Value representing a white stone
# --- GUI configuration ---
CELL_SIZE = 40           # Pixel distance between two adjacent intersections
MARGIN = 30              # Pixel padding around the board edges
STONE_RADIUS = 17        # Pixel radius of a drawn stone
CANVAS_SIZE = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)  # Canvas width/height
# --- Colors (RGB hex strings for tkinter) ---
COLOR_BACKGROUND = "#E8C88F"     # Wooden board background
COLOR_GRID_LINE = "#5A3A1A"      # Grid line color
COLOR_STAR_POINT = "#5A3A1A"     # Star point marker color
COLOR_BLACK_STONE = "#000000"    # Black stone fill
COLOR_WHITE_STONE = "#FFFFFF"    # White stone fill
COLOR_STONE_OUTLINE = "#333333"  # Outline color for stones
COLOR_LAST_MOVE = "#FF0000"      # Marker highlighting the last move
COLOR_WIN_LINE = "#FF4500"       # Line drawn through winning stones
COLOR_STATUS_BG = "#F5F0E1"      # Status bar background
# --- Star points (traditional markers on a 15x15 board) ---
STAR_POINTS = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
# --- Text labels ---
BLACK_NAME = "Black"
WHITE_NAME = "White"