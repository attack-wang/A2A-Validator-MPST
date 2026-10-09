'''Global configuration constants for the match-3 puzzle game.'''
# Window / layout
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 800
FPS = 60
# Board
GRID_SIZE = 8            # 8x8 board
CELL_SIZE = 64
BOARD_PIXEL_SIZE = GRID_SIZE * CELL_SIZE  # 512
BOARD_TOP_LEFT = ((WINDOW_WIDTH - BOARD_PIXEL_SIZE) // 2, 150)
# Candies
NUM_CANDY_TYPES = 6
# Colors (R, G, B)
BACKGROUND_COLOR = (30, 30, 46)
PANEL_COLOR = (49, 50, 68)
CELL_COLOR_A = (58, 60, 80)
CELL_COLOR_B = (52, 54, 72)
BORDER_COLOR = (137, 180, 250)
TEXT_COLOR = (205, 214, 244)
ACCENT_COLOR = (166, 227, 161)
SUBTEXT_COLOR = (147, 153, 178)
DANGER_COLOR = (243, 139, 168)
CANDY_COLORS = [
    (243, 139, 168),  # red - circle
    (250, 179, 135),  # orange - rounded square
    (249, 226, 175),  # yellow - diamond
    (166, 227, 161),  # green - hexagon
    (137, 180, 250),  # blue - star
    (203, 166, 247),  # purple - triangle
]
CANDY_DARK_COLORS = [tuple(max(0, int(v * 0.6)) for v in c) for c in CANDY_COLORS]
# Gameplay
INITIAL_MOVES = 30
TIME_LIMIT_SECONDS = 120
TARGET_SCORE = 2500
SCORE_PER_CANDY = 50
MATCH_BONUS_4 = 100
MATCH_BONUS_5_PLUS = 250
# Animation timings (seconds)
SWAP_DURATION = 0.18
CLEAR_DURATION = 0.22
FALL_GRAVITY = 3000.0  # pixels per second^2
MAX_FALL_SPEED = 1400.0
# Hint
HINT_DELAY = 6.0