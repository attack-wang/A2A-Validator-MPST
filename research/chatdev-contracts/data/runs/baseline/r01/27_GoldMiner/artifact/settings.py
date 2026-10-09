"""Global settings and constants for the Gold Miner game."""
import math
# Screen
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Gold Miner"
# Colors
SKY_COLOR = (135, 206, 235)
SUN_COLOR = (255, 215, 0)
DIRT_COLOR = (139, 94, 52)
DIRT_DARK = (101, 67, 33)
GRASS_COLOR = (60, 140, 60)
ROPE_COLOR = (60, 40, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
ORANGE = (255, 165, 0)
GOLD_COLOR = (255, 200, 40)
GOLD_DARK = (200, 150, 20)
ROCK_COLOR = (130, 130, 130)
ROCK_DARK = (90, 90, 90)
DIAMOND_COLOR = (120, 220, 255)
DIAMOND_DARK = (60, 170, 220)
TNT_RED = (200, 40, 40)
TNT_DARK = (150, 20, 20)
BONE_COLOR = (230, 220, 190)
BAG_COLOR = (120, 80, 40)
GREEN = (60, 180, 80)
UI_BG = (40, 30, 20)
# Layout
GROUND_Y = 150          # y of grass line; pivot sits on it
PIVOT = (WIDTH // 2, GROUND_Y + 10)
ROPE_MIN = 40
ROPE_MAX = 430
CLAW_SIZE = 10
# Claw physics
BASE_SWING = 1.4        # rad/s at level 1
SWING_STEP = 0.12       # extra rad/s per level
MAX_SWING = 2.6
CLAW_EXTEND_SPEED = 550.0   # px/s
CLAW_RETRACT_EMPTY = 450.0  # px/s
CLAW_RETRACT_BASE = 900.0   # px/s * weight divisor
CLAW_RETRACT_MIN = 90.0     # slowest allowed reel-in
SWING_LIMIT = math.radians(78)
# TNT
TNT_FUSE = 1.0          # seconds on claw before detonation
TNT_BLAST_RADIUS = 90
TNT_PENALTY = 50
# Mystery bag
MYSTERY_VALUES = [50, 100, 200, 500, -100]
# Level difficulty
BASE_TARGET = 500
TARGET_STEP = 350
BASE_TIME = 60
MIN_TIME = 25
TIME_PER_LEVEL = 4
BASE_OBJECTS = 10
OBJECTS_PER_LEVEL = 2
MAX_OBJECTS = 22
MAX_TNT = 5