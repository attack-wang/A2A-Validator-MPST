'''
settings.py
Global configuration for the Gold Miner game: screen layout, colors,
claw physics, object specifications and the per-level difficulty curve.
'''
import math
# Screen / timing
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Gold Miner"
# Layout zones
HUD_HEIGHT = 64
GROUND_Y = 150
MINE_TOP = GROUND_Y + 60
MINE_MARGIN = 40
# Colors
SKY_COLOR = (135, 206, 235)
GRASS_COLOR = (76, 145, 65)
DIRT_COLOR = (101, 67, 33)
DIRT_DARK = (85, 55, 27)
ROPE_COLOR = (60, 40, 20)
CLAW_COLOR = (180, 180, 190)
CLAW_DARK = (110, 110, 120)
GOLD_COLOR = (255, 200, 40)
GOLD_DARK = (200, 150, 20)
ROCK_COLOR = (130, 130, 135)
ROCK_DARK = (95, 95, 100)
DIAMOND_COLOR = (120, 220, 255)
DIAMOND_DARK = (70, 170, 220)
BONE_COLOR = (235, 225, 200)
TNT_COLOR = (200, 40, 40)
TNT_DARK = (140, 20, 20)
BAG_COLOR = (150, 100, 60)
HUD_BG = (40, 40, 55)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (230, 60, 60)
GREEN = (80, 200, 90)
YELLOW = (255, 220, 60)
GREY = (170, 170, 170)
ORANGE = (255, 150, 50)
# Claw physics
PIVOT = (SCREEN_WIDTH // 2, GROUND_Y - 10)
SWING_MIN_ANGLE = 20.0
SWING_MAX_ANGLE = 160.0
MIN_ROPE_LENGTH = 60
MAX_ROPE_LENGTH = 640
EXTEND_SPEED = 420.0
RETRACT_SPEED_EMPTY = 520.0
RETRACT_SPEED_LOADED = 700.0
RETRACT_SPEED_MIN = 120.0
CARRY_OFFSET = 12
# Object specs
OBJECT_SPECS = {
    'gold_small': {'value': 50, 'weight': 1.6, 'radius': 14},
    'gold_medium': {'value': 150, 'weight': 3.2, 'radius': 22},
    'gold_large': {'value': 500, 'weight': 6.0, 'radius': 32},
    'rock_small': {'value': 20, 'weight': 4.5, 'radius': 18},
    'rock_large': {'value': 30, 'weight': 7.5, 'radius': 28},
    'diamond': {'value': 600, 'weight': 1.4, 'radius': 16},
    'bone': {'value': 10, 'weight': 1.0, 'radius': 15},
    'tnt': {'value': 0, 'weight': 1.0, 'radius': 20},
    'bag': {'value': 0, 'weight': 2.5, 'radius': 18},
}
def level_config(level):
    goal = 450 + (level - 1) * 300
    time_limit = max(60 - (level - 1) * 5, 25)
    swing_speed = min(55 + (level - 1) * 6, 110)
    counts = {
        'gold_small': 4 + level // 2,
        'gold_medium': 3 + (level - 1) // 3,
        'gold_large': 1 + (level - 1) // 4,
        'rock_small': 2 + level // 2,
        'rock_large': 1 + (level - 1) // 2,
        'diamond': 1 if level >= 2 else 0,
        'bone': 1 + level // 3,
        'tnt': (level - 1) // 2,
        'bag': 1 if level >= 3 else 0,
    }
    return {'goal': goal, 'time_limit': time_limit,
            'swing_speed': swing_speed, 'counts': counts}