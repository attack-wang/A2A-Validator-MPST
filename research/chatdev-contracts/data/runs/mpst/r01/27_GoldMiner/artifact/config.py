"""Configuration constants for the Gold Miner game."""
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Gold Miner"
HUD_HEIGHT = 70
GROUND_Y = 150
MINING_TOP = GROUND_Y + 30
MINING_BOTTOM = SCREEN_HEIGHT - 20
MINING_LEFT = 30
MINING_RIGHT = SCREEN_WIDTH - 30
CLAW_PIVOT_X = SCREEN_WIDTH // 2
CLAW_PIVOT_Y = GROUND_Y - 10
CLAW_MIN_ANGLE = -75.0
CLAW_MAX_ANGLE = 75.0
CLAW_SWING_SPEED = 70.0
CLAW_EXTEND_SPEED = 420.0
CLAW_RETRACT_SPEED = 500.0
CLAW_MAX_LENGTH = 700.0
ROPE_REEL_BASE_SPEED = 160.0
START_TIME = 60.0
TIME_PER_LEVEL_DECREASE = 5.0
MIN_TIME = 30.0
BASE_TARGET = 350
TARGET_STEP = 250
TNT_BLAST_RADIUS = 90
OBJECT_STATS = {
    "gold_small":  {"value": 50,  "weight": 1.0, "radius": 10},
    "gold_medium": {"value": 150, "weight": 2.2, "radius": 16},
    "gold_large":  {"value": 500, "weight": 4.0, "radius": 24},
    "diamond":     {"value": 600, "weight": 1.2, "radius": 12},
    "rock_small":  {"value": 20,  "weight": 1.6, "radius": 12},
    "rock_large":  {"value": 30,  "weight": 3.8, "radius": 22},
    "bone":        {"value": 15,  "weight": 1.3, "radius": 12},
    "tnt":         {"value": 0,   "weight": 1.0, "radius": 14},
    "mystery_bag": {"value": 0,   "weight": 1.6, "radius": 14},
}
COLOR_BG = (21, 26, 34)
COLOR_DIRT = (94, 66, 41)
COLOR_DIRT_DARK = (74, 52, 33)
COLOR_ROPE = (230, 220, 190)
COLOR_GOLD = (255, 205, 60)
COLOR_GOLD_DARK = (180, 130, 20)
COLOR_ROCK = (130, 130, 135)
COLOR_ROCK_DARK = (95, 95, 100)
COLOR_DIAMOND = (120, 220, 255)
COLOR_BONE = (235, 225, 205)
COLOR_TNT = (200, 60, 50)
COLOR_BAG = (150, 100, 60)
COLOR_TEXT = (240, 240, 240)
COLOR_GOOD = (120, 255, 140)
COLOR_BAD = (255, 110, 90)
COLOR_HUD_BG = (40, 46, 58)
COLOR_GROUND = (120, 90, 55)
COLOR_CLAW = (200, 200, 210)
COLOR_CLAW_DARK = (120, 120, 130)