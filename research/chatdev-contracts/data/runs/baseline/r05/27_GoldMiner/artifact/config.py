'''
Configuration constants and shared helpers for the Gold Miner game.
'''
import math
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60
# Colors (R, G, B)
COLOR_BG = (30, 20, 10)          # dirt background
COLOR_SKY = (135, 206, 235)      # sky above ground
COLOR_DIRT = (101, 67, 33)
COLOR_DIRT_DARK = (80, 50, 25)
COLOR_ROPE = (60, 40, 20)
COLOR_GOLD = (255, 200, 40)
COLOR_GOLD_DARK = (200, 140, 20)
COLOR_ROCK = (130, 130, 130)
COLOR_ROCK_DARK = (90, 90, 90)
COLOR_DIAMOND = (80, 220, 255)
COLOR_DIAMOND_DARK = (40, 160, 200)
COLOR_TNT = (200, 40, 40)
COLOR_TNT_DARK = (140, 25, 25)
COLOR_BONE = (230, 225, 200)
COLOR_TEXT = (255, 255, 255)
COLOR_HUD_BG = (20, 20, 30)
COLOR_TARGET = (80, 255, 80)
COLOR_TIME_LOW = (255, 80, 80)
COLOR_CLAW = (185, 185, 195)
COLOR_LABEL = (255, 255, 120)
# Layout
GROUND_Y = 120            # y of the ground line; mine is below
HUD_HEIGHT = 48
STATUS_BAR_HEIGHT = 28
# Claw settings
CLAW_PIVOT_X = SCREEN_WIDTH // 2
CLAW_PIVOT_Y = 60
CLAW_SWING_AMPLITUDE = 75   # degrees, max swing angle from vertical
CLAW_SWING_SPEED = 1.6      # angular frequency (radians per second)
CLAW_EXTEND_SPEED = 420     # pixels per second while extending
CLAW_RETRACT_EMPTY_SPEED = 700
CLAW_RETRACT_BASE_SPEED = 260   # reel speed for weight 1
CLAW_MIN_LENGTH = 40
CLAW_MAX_LENGTH = 900
# Object definitions: kind -> properties
OBJECT_TYPES = {
    "gold_small":  {"value": 50,  "weight": 1, "radius": 12},
    "gold_medium": {"value": 150, "weight": 2, "radius": 18},
    "gold_large":  {"value": 500, "weight": 4, "radius": 26},
    "diamond":     {"value": 600, "weight": 1, "radius": 13},
    "rock_small":  {"value": 11,  "weight": 2, "radius": 14},
    "rock_large":  {"value": 20,  "weight": 4, "radius": 24},
    "bone":        {"value": 30,  "weight": 2, "radius": 15},
    "tnt":         {"value": 0,   "weight": 1, "radius": 16},
}
# Vertical placement bands (fraction of the mine depth per kind)
DEPTH_RANGES = {
    "gold_small": (0.10, 0.55),
    "gold_medium": (0.30, 0.80),
    "gold_large": (0.55, 0.95),
    "diamond": (0.60, 0.95),
    "rock_small": (0.10, 0.90),
    "rock_large": (0.30, 0.95),
    "bone": (0.15, 0.85),
    "tnt": (0.20, 0.90),
}
# Explosion
EXPLOSION_RADIUS = 100
# Level difficulty
LEVEL_BASE_TARGET = 500
LEVEL_TARGET_STEP = 350
LEVEL_BASE_TIME = 60.0
LEVEL_TIME_STEP = 5.0
LEVEL_MIN_TIME = 30.0
# Mine playable band
MINE_TOP = GROUND_Y + 30
MINE_BOTTOM = SCREEN_HEIGHT - STATUS_BAR_HEIGHT - 30
def distance(a, b):
    """Return the Euclidean distance between two (x, y) points."""
    return math.hypot(a[0] - b[0], a[1] - b[1])