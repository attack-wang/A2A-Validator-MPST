'''
Central configuration for the 2048 game: board settings, colors, and fonts.
Keeping these values in one place makes it easy to re-theme or resize the game.
'''
# ---------------------------------------------------------------------------
# Game settings
# ---------------------------------------------------------------------------
GRID_SIZE = 4            # Number of rows/columns on the board (standard 2048 is 4x4)
TWO_PROBABILITY = 0.9    # Chance a spawned tile is a 2 (otherwise it is a 4)
INITIAL_TILES = 2        # Number of tiles present when a game starts
# ---------------------------------------------------------------------------
# Window / layout settings
# ---------------------------------------------------------------------------
WINDOW_TITLE = "2048"
WINDOW_BG = "#faf8ef"        # Warm off-white page background
GRID_BG = "#bbada0"          # Beige board background
CELL_PADX = 5                # Horizontal padding around each cell
CELL_PADY = 5                # Vertical padding around each cell
GRID_PAD = 15                # Outer padding around the board
HEADER_PAD = 15              # Padding for the header area
# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
TITLE_FONT = ("Helvetica", 40, "bold")
SCORE_LABEL_FONT = ("Helvetica", 10, "bold")
SCORE_VALUE_FONT = ("Helvetica", 16, "bold")
TILE_FONT_LARGE = ("Helvetica", 28, "bold")   # 1-2 digit tiles
TILE_FONT_MEDIUM = ("Helvetica", 24, "bold")  # 3 digit tiles
TILE_FONT_SMALL = ("Helvetica", 18, "bold")   # 4+ digit tiles
INSTRUCTION_FONT = ("Helvetica", 11)
GAME_OVER_FONT = ("Helvetica", 28, "bold")
# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
TEXT_COLOR = "#776e65"          # Standard brownish text color
EMPTY_CELL_BG = "#cdc1b4"       # Color of an empty cell
SCORE_BOX_BG = "#bbada0"        # Background of score boxes
SCORE_LABEL_FG = "#eee4da"      # Score box caption color
SCORE_VALUE_FG = "#ffffff"      # Score box value color
BUTTON_BG = "#8f7a66"           # "New Game" button background
BUTTON_FG = "#f9f6f2"           # "New Game" button text
GAME_OVER_BG = "#eee4da"        # Game-over overlay background
GAME_OVER_TEXT_FG = "#776e65"   # Game-over overlay text color
# Tile colors: tile value -> (background, foreground)
TILE_COLORS = {
    2:    ("#eee4da", "#776e65"),
    4:    ("#ede0c8", "#776e65"),
    8:    ("#f2b179", "#f9f6f2"),
    16:   ("#f59563", "#f9f6f2"),
    32:   ("#f67c5f", "#f9f6f2"),
    64:   ("#f65e3b", "#f9f6f2"),
    128:  ("#edcf72", "#f9f6f2"),
    256:  ("#edcc61", "#f9f6f2"),
    512:  ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}
# Fallback colors for tiles above 2048 (4096, 8192, ...)
DEFAULT_TILE_COLORS = ("#3c3a32", "#f9f6f2")