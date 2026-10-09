'''
Configuration constants for the 2048 game.
Defines window dimensions, grid geometry, the color palette for tiles,
and gameplay parameters. Colors are stored as hex strings so they can be
used directly by the standard-library tkinter renderer, removing the
dependency on third-party packages such as pygame.
'''
# ---------------------------------------------------------------------------
# Window / layout settings
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 480          # Total window width in pixels
WINDOW_HEIGHT = 620         # Total window height in pixels
GRID_SIZE = 4               # Number of rows/columns on the board
CELL_SIZE = 100             # Side length of one board cell in pixels
CELL_PADDING = 10           # Gap between cells in pixels
OUTER_MARGIN = 15           # Margin around the grid inside the window
GRID_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_PADDING   # 450
GRID_LEFT = (WINDOW_WIDTH - GRID_WIDTH) // 2                          # 15
GRID_TOP = 150              # Y coordinate where the grid begins
# ---------------------------------------------------------------------------
# Colors as hex strings (original RGB values noted in the comments)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = '#BBADA0'      # Classic 2048 beige background (187,173,160)
COLOR_EMPTY_CELL = '#CDC1B4'      # Empty cell color (205,193,180)
COLOR_TEXT_DARK = '#776E65'       # Dark text on light tiles (119,110,101)
COLOR_TEXT_LIGHT = '#F9F6F2'      # Light text on dark tiles (249,246,242)
COLOR_OVERLAY = '#EEE4DA'         # Game-over overlay base color (238,228,218)
COLOR_BOX = '#CDC1B4'             # Score box background (205,193,180)
# Tile background colors keyed by tile value; values above the last key
# fall back to the "super" color.
TILE_COLORS = {
    2:    '#EEE4DA',
    4:    '#EDE3C1',
    8:    '#F2B179',
    16:   '#F59563',
    32:   '#F67C5F',
    64:   '#F65E3B',
    128:  '#EDCF72',
    256:  '#EDCC61',
    512:  '#EDC850',
    1024: '#EDC53F',
    2048: '#EDC22E',
}
TILE_COLOR_SUPER = '#3C3A32'      # For tiles above 2048 (4096, 8192, ...)
# ---------------------------------------------------------------------------
# Gameplay parameters
# ---------------------------------------------------------------------------
TWO_PROBABILITY = 0.9       # Chance a spawned tile is a 2 (otherwise a 4)
STARTING_TILES = 2          # Number of tiles on the board at game start