'''
constants.py
Central place for every tunable constant of the Gomoku game: board
dimensions, player identifiers, game states, GUI geometry and colors.
'''
# ----------------------------------------------------------------------
# Board configuration
# ----------------------------------------------------------------------
BOARD_SIZE = 15          # Standard Gomoku board: 15x15 intersections
STONES_TO_WIN = 5        # Aligned stones required for a victory
# ----------------------------------------------------------------------
# Cell / player values
# ----------------------------------------------------------------------
EMPTY = 0
BLACK = 1
WHITE = 2
PLAYER_NAMES = {
    BLACK: "Black",
    WHITE: "White",
}
# ----------------------------------------------------------------------
# Game states
# ----------------------------------------------------------------------
ONGOING = "ongoing"
BLACK_WINS = "black_wins"
WHITE_WINS = "white_wins"
DRAW = "draw"
# ----------------------------------------------------------------------
# Win checking directions: (row delta, col delta)
# ----------------------------------------------------------------------
DIRECTIONS = [
    (0, 1),    # horizontal
    (1, 0),    # vertical
    (1, 1),    # diagonal (top-left -> bottom-right)
    (1, -1),   # diagonal (top-right -> bottom-left)
]
# ----------------------------------------------------------------------
# GUI geometry
# ----------------------------------------------------------------------
CELL_SIZE = 40           # Pixel distance between two adjacent intersections
MARGIN = 30              # Pixel margin around the playing grid
STONE_RADIUS = 16        # Radius of a stone in pixels
WINDOW_WIDTH = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)
WINDOW_HEIGHT = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)
# ----------------------------------------------------------------------
# Colors
# ----------------------------------------------------------------------
COLOR_BACKGROUND = "#DCB35C"        # Wooden board color
COLOR_GRID_LINE = "#7A4A1F"         # Grid line color
COLOR_STAR_POINT = "#3B2412"        # Traditional star points
COLOR_BLACK_STONE = "#101010"
COLOR_WHITE_STONE = "#FAFAFA"
COLOR_WHITE_STONE_EDGE = "#7F7F7F"
COLOR_LAST_MOVE_MARK = "#E53E3E"    # Cross marker on the latest stone
COLOR_WIN_HIGHLIGHT = "#3182CE"     # Highlight around winning stones
COLOR_STATUS_BG = "#F5EBD7"
COLOR_STATUS_FG = "#3B2412"
COLOR_BUTTON_BG = "#2F855A"
COLOR_BUTTON_BG_ACTIVE = "#276749"
COLOR_BUTTON_FG = "#FFFFFF"