"""
settings.py
Global configuration constants for the Gold Miner game.
"""
# --- Screen / timing -------------------------------------------------------
TITLE = "Gold Miner"
WIDTH = 800
HEIGHT = 600
FPS = 60
# --- Layout ----------------------------------------------------------------
PIVOT_X = WIDTH // 2          # claw pivot (top centre)
PIVOT_Y = 70
GROUND_Y = 150                # y of the soil surface
ROPE_IDLE = 55                # rope length while swinging
MAX_ROPE = 660                # maximum rope extension
MAX_ANGLE = 78.0              # swing amplitude in degrees (from vertical)
CLAW_SIZE = 15                # claw head size in px
# --- Claw motion -----------------------------------------------------------
EXTEND_SPEED = 560.0          # px/s while shooting out
EMPTY_RETRACT_SPEED = 780.0   # px/s returning empty
BASE_REEL_SPEED = 470.0       # px/s when reeling an object of weight 1.0
SWING_SPEED_BASE = 85.0       # deg/s at level 1
SWING_SPEED_PER_LEVEL = 6.0   # extra deg/s per level
SWING_SPEED_MAX = 150.0
# --- Level rules -----------------------------------------------------------
LEVEL_TIME_BASE = 60.0
LEVEL_TIME_STEP = 2.0         # seconds removed per level
LEVEL_TIME_MIN = 40.0
GOAL_START_FRACTION = 0.45    # goal = fraction of total item value
GOAL_FRACTION_STEP = 0.025    # fraction growth per level
GOAL_MAX_FRACTION = 0.65
TIME_BONUS_PER_SECOND = 5     # bonus gold for finishing early
# --- TNT -------------------------------------------------------------------
TNT_PENALTY = 75
TNT_BLAST_RADIUS = 110
# --- Colors ----------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
SKY_TOP = (120, 190, 250)
SKY_BOTTOM = (200, 232, 255)
SUN_COLOR = (255, 220, 90)
CLOUD_COLOR = (245, 250, 255)
GRASS = (74, 155, 66)
DIRT = (146, 100, 54)
DIRT_DARK = (118, 79, 40)
DIRT_SPECK = (104, 68, 34)
GOLD = (255, 190, 40)
GOLD_DARK = (200, 140, 20)
GOLD_SHINE = (255, 240, 170)
STONE = (150, 150, 155)
STONE_DARK = (110, 110, 118)
DIAMOND = (90, 220, 235)
DIAMOND_DARK = (40, 160, 190)
BONE = (240, 238, 220)
TNT_RED = (200, 40, 40)
TNT_DARK = (150, 25, 25)
FUSE = (90, 60, 30)
MYSTERY = (170, 110, 220)
ROPE_COLOR = (60, 40, 20)
CLAW_COLOR = (70, 70, 80)
HUD_PANEL = (25, 30, 45)
HUD_TEXT = (255, 255, 255)
GOLD_TEXT = (255, 210, 60)
TIME_LOW = (255, 80, 80)
GOOD_GREEN = (90, 200, 90)
BAD_RED = (230, 70, 70)
OVERLAY = (10, 10, 20)