'''
config.py
Central configuration for the 2048 game: window dimensions, grid geometry,
color palette, font sizes, and frame-rate settings. Keeping all tunable
constants in one place makes the game easy to restyle or resize.
'''
# ---------------------------------------------------------------------------
# Window / layout
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 600          # Main window width in pixels
WINDOW_HEIGHT = 700         # Main window height in pixels
WINDOW_CAPTION = "2048"     # Title shown in the window's title bar
# ---------------------------------------------------------------------------
# Grid geometry
# ---------------------------------------------------------------------------
GRID_SIZE = 4               # 4x4 playing grid
CELL_SIZE = 120             # Pixel size of a single cell
CELL_GAP = 10               # Pixel spacing between cells
GRID_TOP = 160              # Y coordinate where the grid area begins
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (250, 248, 238)      # Window background (beige)
COLOR_GRID_CONTAINER = (187, 173, 160)  # Grid container (brown-grey)
COLOR_CELL_EMPTY = (205, 193, 180)      # Empty cell
COLOR_TEXT_DARK = (119, 110, 101)       # Dark text (on light tiles)
COLOR_TEXT_LIGHT = (249, 246, 242)      # Light text (on colored tiles)
# Tile colors: value -> (background_color, text_color)
TILE_COLORS = {
    2:    ((238, 228, 218), COLOR_TEXT_DARK),
    4:    ((237, 224, 200), COLOR_TEXT_DARK),
    8:    ((242, 177, 121), COLOR_TEXT_LIGHT),
    16:   ((245, 149, 99),  COLOR_TEXT_LIGHT),
    32:   ((246, 124, 95),  COLOR_TEXT_LIGHT),
    64:   ((246, 94, 59),   COLOR_TEXT_LIGHT),
    128:  ((237, 207, 114), COLOR_TEXT_LIGHT),
    256:  ((237, 204, 97),  COLOR_TEXT_LIGHT),
    512:  ((237, 200, 80),  COLOR_TEXT_LIGHT),
    1024: ((237, 197, 63),  COLOR_TEXT_LIGHT),
    2048: ((237, 194, 46),  COLOR_TEXT_LIGHT),
}
# Fallback color for tiles above 2048 (4096, 8192, ...)
DEFAULT_TILE_COLOR = ((60, 58, 50), COLOR_TEXT_LIGHT)
# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONT_NAME = None            # None -> pygame's built-in default font
FONT_SIZE_TILE_2_DIGITS = 48
FONT_SIZE_TILE_3_DIGITS = 40
FONT_SIZE_TILE_4_DIGITS = 32
FONT_SIZE_TILE_5_DIGITS = 24
FONT_SIZE_SCORE = 20
FONT_SIZE_TITLE = 44
FONT_SIZE_MESSAGE = 52
# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------
FPS = 60                    # Maximum frames per second