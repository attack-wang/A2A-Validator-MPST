'''
settings.py
Central configuration module for the Space Invaders game.
Contains all tunable constants: screen dimensions, colours, gameplay
speeds, fleet layout, scoring values and HUD options. Keeping every
magic number in one place makes the game easy to tweak and balance.
'''
# ---------------------------------------------------------------------------
# Window / timing
# ---------------------------------------------------------------------------
TITLE = "Space Invaders"
SCREEN_WIDTH = 820
SCREEN_HEIGHT = 640
FPS = 60
# ---------------------------------------------------------------------------
# Colours (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (8, 10, 24)
COLOR_TEXT = (235, 235, 235)
COLOR_PLAYER = (80, 220, 120)
COLOR_BULLET = (240, 240, 160)
COLOR_BOMB = (240, 90, 90)
# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
PLAYER_PIXEL = 3
PLAYER_SPEED = 4.5
PLAYER_START_LIVES = 3
PLAYER_FIRE_COOLDOWN = 400
PLAYER_RESPAWN_INVINCIBILITY = 1500
# ---------------------------------------------------------------------------
# Projectiles
# ---------------------------------------------------------------------------
BULLET_SPEED = 9.0
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
BOMB_SPEED = 3.2
BOMB_WIDTH = 4
BOMB_HEIGHT = 12
BOMB_TIMER_MIN = 500
BOMB_TIMER_MAX = 1300
BOMB_INTERCEPT_POINTS = 5
# ---------------------------------------------------------------------------
# Alien fleet
# ---------------------------------------------------------------------------
ALIEN_ROWS = 5
ALIEN_COLS = 11
ALIEN_PIXEL = 3
ALIEN_H_SPACING = 48
ALIEN_V_SPACING = 42
FLEET_TOP_MARGIN = 90
FLEET_SIDE_MARGIN = 30
FLEET_STEP_DOWN = 18
FLEET_BASE_SPEED = 0.55
FLEET_SPEED_INCREMENT = 0.10
FLEET_MAX_SPEED = 6.0
FLEET_ANIMATION_INTERVAL = 500
# Sprite type (index into bitmaps.ALIEN_FRAMES) and colour per fleet row.
ALIEN_ROW_TYPES = (0, 1, 1, 2, 2)
ALIEN_ROW_COLORS = (
    (180, 110, 240),   # top row (squid)
    (90, 200, 250),    # second row (crab)
    (90, 200, 250),
    (110, 230, 110),   # bottom rows (octopus)
    (110, 230, 110),
)
# Points awarded per alien, indexed by row (0 = top row).
ALIEN_POINTS = (30, 20, 20, 10, 10)
# If any alien's bottom edge reaches this Y the invasion succeeds.
INVASION_LINE_Y = SCREEN_HEIGHT - 90
# ---------------------------------------------------------------------------
# HUD / fonts
# ---------------------------------------------------------------------------
FONT_NAME = None
FONT_SIZE_SMALL = 18
FONT_SIZE_MEDIUM = 26
FONT_SIZE_LARGE = 48
HUD_MARGIN = 12