'''
config.py
Central configuration module for the Gomoku application.
This file stores every tunable constant used across the project so that
the look & feel of the game (board size, colours, stone radius, fonts,
window title, etc.) can be adjusted from a single place without touching
the game logic or the GUI code.
'''
# ---------------------------------------------------------------------------
# Board geometry
# ---------------------------------------------------------------------------
BOARD_SIZE = 15          # Number of intersections per side (standard Gomoku).
CELL_SIZE = 40           # Pixel distance between two adjacent intersections.
MARGIN = 36              # Pixel padding around the grid (room for labels).
STONE_RADIUS = 16        # Radius (pixels) of a stone.
STAR_POINTS = ((3, 3), (3, 11), (11, 3), (11, 11), (7, 7))  # Hoshi points.
# Derived canvas dimensions.
CANVAS_SIZE = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)
# ---------------------------------------------------------------------------
# Players
# ---------------------------------------------------------------------------
EMPTY = 0
PLAYER_BLACK = 1
PLAYER_WHITE = 2
# ---------------------------------------------------------------------------
# Colours (hex strings understood by Tkinter)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = "#F4E9D3"       # Window / frame background (parchment).
COLOR_BOARD = "#DCB35C"            # Classic wooden Go-board colour.
COLOR_GRID_LINE = "#5A3A1A"        # Dark brown grid lines.
COLOR_STAR_POINT = "#3B2410"       # Star points (slightly darker than lines).
COLOR_LABEL = "#5A3A1A"            # Coordinate labels.
COLOR_BLACK_STONE = "#101010"      # Black stone fill.
COLOR_BLACK_HIGHLIGHT = "#4A4A4A"  # Small shine on black stones.
COLOR_WHITE_STONE = "#FAFAFA"      # White stone fill.
COLOR_WHITE_OUTLINE = "#333333"    # Outline of white stones.
COLOR_LAST_MOVE = "#D23B2E"        # Marker for the most recent move.
COLOR_WIN_RING = "#E8442A"         # Ring drawn around winning stones.
COLOR_STATUS_BLACK = "#101010"
COLOR_STATUS_WHITE = "#6E6E6E"     # Readable grey for white-player text.
COLOR_STATUS_WIN = "#B22222"       # Firebrick for win messages.
COLOR_BUTTON_BG = "#8B5A2B"        # Button background (wood tone).
COLOR_BUTTON_FG = "#FFFFFF"        # Button text.
COLOR_BUTTON_ACTIVE = "#A9702F"    # Button background when hovered/pressed.
# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONT_STATUS = ("Helvetica", 13, "bold")
FONT_BUTTON = ("Helvetica", 11, "bold")
FONT_COORDINATE = ("Helvetica", 8)
# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------
WINDOW_TITLE = "Gomoku — Five in a Row"
CLICK_TOLERANCE = 0.45 * CELL_SIZE  # Max distance click-to-intersection.