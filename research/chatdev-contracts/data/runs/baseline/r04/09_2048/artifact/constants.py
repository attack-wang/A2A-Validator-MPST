'''
constants.py
Defines global configuration constants for the 2048 game, including
window dimensions, board geometry, colors, fonts, and tile color mapping.
'''
# ------------------------------------------------------------------
# Window / board geometry
# ------------------------------------------------------------------
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 602
GRID_SIZE = 4
CELL_SIZE = 100
CELL_PADDING = 8
BOARD_PADDING = 10
# Derived board geometry (single source of truth for the canvas size)
BOARD_WIDTH = 2 * BOARD_PADDING + GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * CELL_PADDING  # 444
BOARD_HEIGHT = BOARD_WIDTH
WINDOW_MARGIN = 28
# ------------------------------------------------------------------
# Colors
# ------------------------------------------------------------------
WINDOW_BG_COLOR = "#faf8ef"
BOARD_COLOR = "#bbada0"
EMPTY_CELL_COLOR = "#cdc1b4"
TEXT_COLOR_DARK = "#776e65"
TEXT_COLOR_LIGHT = "#f9f6f2"
SCORE_LABEL_COLOR = "#776e65"
SCORE_VALUE_COLOR = "#ffffff"
SCORE_BOX_COLOR = "#bbada0"
DEFAULT_TILE_COLOR = "#3c3a32"
NEW_TILE_BORDER_COLOR = "#f67c5f"
GAME_OVER_OVERLAY_COLOR = "#bbada0"
BUTTON_BG_COLOR = "#8f7a66"
BUTTON_FG_COLOR = "#f9f6f2"
# ------------------------------------------------------------------
# Fonts
# ------------------------------------------------------------------
FONT_FAMILY = "Helvetica"
TITLE_FONT_SIZE = 40
SCORE_LABEL_FONT_SIZE = 10
SCORE_VALUE_FONT_SIZE = 18
BUTTON_FONT_SIZE = 11
# ------------------------------------------------------------------
# Tile value -> background color mapping (classic 2048 palette)
# ------------------------------------------------------------------
TILE_COLORS = {
    2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
    32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
    512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
    4096: "#3c3a32", 8192: "#3c3a32", 16384: "#3c3a32",
}