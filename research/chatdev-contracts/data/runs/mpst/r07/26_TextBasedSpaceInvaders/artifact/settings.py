'''
settings.py
Central configuration for the simplified Space Invaders game.
Every tunable value (screen size, speeds, colors, fleet layout,
scoring, lives...) is defined here so gameplay can be balanced
from a single place without touching the game logic.
'''
# ------------------------------------------------------------------
# Screen / timing
# ------------------------------------------------------------------
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"
# ------------------------------------------------------------------
# Colors
# ------------------------------------------------------------------
BLACK = (12, 12, 24)
WHITE = (235, 235, 235)
GREEN = (0, 210, 90)
RED = (230, 60, 60)
YELLOW = (250, 220, 70)
CYAN = (70, 220, 220)
ORANGE = (250, 150, 50)
# ------------------------------------------------------------------
# Player ship
# ------------------------------------------------------------------
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 30
PLAYER_SPEED = 5            # pixels per frame
PLAYER_START_X = WIDTH // 2
PLAYER_START_Y = HEIGHT - 40
PLAYER_COOLDOWN = 350       # milliseconds between shots
# ------------------------------------------------------------------
# Player bullets
# ------------------------------------------------------------------
BULLET_SPEED = -9           # negative = upwards
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
BULLET_COLOR = GREEN
# ------------------------------------------------------------------
# Alien bombs
# ------------------------------------------------------------------
BOMB_SPEED = 4              # pixels per frame (downwards)
BOMB_WIDTH = 4
BOMB_HEIGHT = 12
BOMB_COLOR = RED
BOMB_CHANCE = 0.002         # per bottom alien, per frame
MAX_BOMBS = 5               # simultaneous bombs on screen
# ------------------------------------------------------------------
# Alien fleet
# ------------------------------------------------------------------
ALIEN_ROWS = 4
ALIEN_COLS = 8
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 28
ALIEN_H_SPACING = 12
ALIEN_V_SPACING = 14
FLEET_TOP_MARGIN = 70
ALIEN_SPEED_X = 1.2         # base horizontal speed (pixels per frame)
ALIEN_DROP_SPEED = 24       # downward step when an edge is reached
DROP_SPEEDUP = 1.06         # fleet speed multiplier after every drop
SHRINK_SPEEDUP = 1.5        # extra speed factor as the fleet shrinks
MAX_FLEET_SPEED = 7.0       # cap so the game stays playable
ALIEN_REACH_Y = HEIGHT - 110  # aliens reaching this line end the game
# Points per alien, indexed by row (top rows are worth more)
ALIEN_POINTS = [30, 20, 20, 10, 10]
# ------------------------------------------------------------------
# Lives / HUD
# ------------------------------------------------------------------
STARTING_LIVES = 3
HUD_FONT_SIZE = 24
BIG_FONT_SIZE = 52
FONT_NAME = None            # None -> pygame's built-in default font