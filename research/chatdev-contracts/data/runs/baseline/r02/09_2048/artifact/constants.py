'''
constants.py
Configuration constants for the 2048 game: board dimensions, window size,
color palette (including per-tile colors), and font sizes.
'''
# ---------------------------------------------------------------------------
# Board and window dimensions
# ---------------------------------------------------------------------------
GRID_SIZE = 4          # 4x4 playing grid
CELL_SIZE = 100        # Pixel size of each cell
CELL_MARGIN = 10       # Gap between cells and around the grid
SCORE_BAR_HEIGHT = 110 # Vertical space reserved for the score bar
HELP_BAR_HEIGHT = 50   # Vertical space reserved for help text
GRID_PANEL_WIDTH = CELL_SIZE * GRID_SIZE + CELL_MARGIN * (GRID_SIZE + 1)   # 450
# FIX: window must be wider than the panel so the right outer margin is not clipped
WINDOW_WIDTH = GRID_PANEL_WIDTH + CELL_MARGIN * 2                          # 470
WINDOW_HEIGHT = (SCORE_BAR_HEIGHT + CELL_SIZE * GRID_SIZE
                 + CELL_MARGIN * (GRID_SIZE + 1) + HELP_BAR_HEIGHT)        # 610
GRID_ORIGIN_X = CELL_MARGIN
GRID_ORIGIN_Y = SCORE_BAR_HEIGHT
FPS = 60
# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
BACKGROUND_COLOR = (187, 173, 160)      # Classic 2048 beige background
GRID_PANEL_COLOR = (187, 173, 160)      # Grid panel background
EMPTY_CELL_COLOR = (205, 193, 180)      # Empty cell slots
TEXT_COLOR = (119, 110, 101)            # Dark text (for light tiles / labels)
LIGHT_TEXT_COLOR = (249, 246, 242)      # Light text (for dark tiles)
OVERLAY_COLOR = (187, 173, 160, 180)    # Semi-transparent game-over overlay
TITLE_COLOR = (119, 110, 101)
# Per-tile colors: value -> (tile_color, text_color)
TILE_COLORS = {
    2:    ((238, 228, 218), TEXT_COLOR),
    4:    ((237, 227, 193), TEXT_COLOR),
    8:    ((242, 177, 121), LIGHT_TEXT_COLOR),
    16:   ((245, 149, 99),  LIGHT_TEXT_COLOR),
    32:   ((246, 124, 95),  LIGHT_TEXT_COLOR),
    64:   ((246, 94, 59),   LIGHT_TEXT_COLOR),
    128:  ((237, 207, 114), LIGHT_TEXT_COLOR),
    256:  ((237, 204, 97),  LIGHT_TEXT_COLOR),
    512:  ((237, 200, 80),  LIGHT_TEXT_COLOR),
    1024: ((237, 197, 63),  LIGHT_TEXT_COLOR),
    2048: ((237, 194, 46),  LIGHT_TEXT_COLOR),
}
DEFAULT_TILE_COLOR = ((60, 58, 50), LIGHT_TEXT_COLOR)  # Tiles above 2048