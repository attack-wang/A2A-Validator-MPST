'''
settings.py
Central configuration module for the simplified Space Invaders game.
All tunable constants (screen size, colors, speeds, alien grid layout,
lives, scoring, HUD fonts, starfield, etc.) live here so gameplay can
be adjusted in one place.
'''
# ---------------------------------------------------------------------------
# Screen / timing
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Simplified Space Invaders"
# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
BLACK = (10, 10, 20)
WHITE = (240, 240, 240)
GREEN = (0, 200, 90)
RED = (230, 60, 60)
BLUE = (70, 130, 255)
CYAN = (0, 210, 210)
PURPLE = (180, 80, 230)
YELLOW = (255, 215, 0)
STAR_COLOR = (200, 200, 220)
# One color per alien row (top row first)
ALIEN_COLORS = [PURPLE, BLUE, CYAN, GREEN]
# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_SPEED = 6                      # pixels per frame
PLAYER_START_LIVES = 3
PLAYER_COLOR = GREEN
PLAYER_Y_OFFSET = 40                  # distance of ship bottom from screen bottom
PLAYER_SHOOT_COOLDOWN_MS = 350
PLAYER_RESPAWN_INVULNERABILITY_MS = 1500
MAX_PLAYER_BULLETS = 3                # max simultaneous player shots
# ---------------------------------------------------------------------------
# Bullets
# ---------------------------------------------------------------------------
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
PLAYER_BULLET_SPEED = -9              # negative = moves upward
ALIEN_BULLET_SPEED = 5
PLAYER_BULLET_COLOR = WHITE
ALIEN_BULLET_COLOR = RED
# ---------------------------------------------------------------------------
# Aliens
# ---------------------------------------------------------------------------
ALIEN_ROWS = 4
ALIEN_COLS = 8
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 30
ALIEN_HORIZONTAL_SPEED = 2            # pixels per frame
ALIEN_DROP_STEP = 20                  # pixels dropped on direction change
ALIEN_TOP_MARGIN = 80
ALIEN_SPACING_X = 60
ALIEN_SPACING_Y = 45
ALIEN_FIRE_COOLDOWN_MS = 800          # minimum time between alien shots
# Grid is horizontally centered on the screen
ALIEN_GRID_WIDTH = (ALIEN_COLS - 1) * ALIEN_SPACING_X + ALIEN_WIDTH
ALIEN_GRID_START_X = (SCREEN_WIDTH - ALIEN_GRID_WIDTH) // 2
# If any alien's bottom edge reaches this line, the invasion succeeds
ALIEN_BOTTOM_LIMIT = SCREEN_HEIGHT - 120
# Scoring: top rows are worth more (row 0 = top)
ALIEN_BASE_SCORE = 10                 # base points, multiplied by remaining rows below
# ---------------------------------------------------------------------------
# HUD / fonts
# ---------------------------------------------------------------------------
FONT_SIZE = 26
BIG_FONT_SIZE = 64
HUD_MARGIN = 10
# ---------------------------------------------------------------------------
# Background starfield
# ---------------------------------------------------------------------------
STAR_COUNT = 60